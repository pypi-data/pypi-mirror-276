import json
import queue
import random
import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from json import JSONDecodeError
from typing import TypedDict, Any, Dict, List, Optional, Tuple, Union, cast
import logging

import websocket
from web3.providers import JSONBaseProvider
from web3.types import RPCEndpoint, RPCResponse

EULITH_SUBSCRIPTION_TYPES = ["uni_prices"]

logger = logging.getLogger("eulith")


class EulithWebsocketRequestHandler(ABC):
    @abstractmethod
    def handle_result(self, message: Dict[Any, Any]) -> Any:
        pass

    @abstractmethod
    def handle_error(self, message: Dict[Any, Any]) -> Any:
        pass


class SubscribeRequest(TypedDict, total=False):
    # if you're using a eulith subscription, you should specify the type here, otherwise leave empty
    # note eth_subscribe requests do not have a subscription_type. These are non-eulith subscriptions
    subscription_type: Optional[str]
    # whatever arguments should be passed in the `params` field of the request
    args: Union[Dict[Any, Any], List[Any]]


class EulithSyncResponse:
    error: Optional[Exception]

    def __init__(self) -> None:
        self.event = threading.Event()
        self.value = None
        self.error = None

    def set_value(self, value: Any) -> None:
        self.value = value
        self.event.set()

    def set_error(self, e: Exception) -> None:
        self.error = e
        self.event.set()

    def get_value(self) -> Any:
        self.event.wait()
        if self.error is not None:
            raise self.error

        return self.value


class SubscriptionDetails:
    subscription_id: Optional[str]

    def __init__(
        self,
        handler: EulithWebsocketRequestHandler,
        resubscribe_payload: Dict[Any, Any],
    ) -> None:
        self.handler = handler
        self.subscription_id = None
        self.resubscribe_payload = resubscribe_payload

    def handle_message(self, data: Dict[Any, Any]) -> Any:
        return self.handler.handle_result(data)

    def handle_error(self, data: Dict[Any, Any]) -> Any:
        return self.handler.handle_error(data)

    def set_subscription_id(self, sub_id: str) -> None:
        self.subscription_id = sub_id

    def get_resubscribe_payload(self) -> Dict[Any, Any]:
        return self.resubscribe_payload


class SubscriptionHandle:
    def __init__(self, sub_details: SubscriptionDetails, eulith_service: Any) -> None:
        self.sub_details = sub_details
        self.eulith_service = eulith_service

    def unsubscribe(self) -> bool:
        return self.eulith_service.unsubscribe(self.sub_details)


class CouldNotConnectException(Exception):
    pass


class ThreadSafeDict:
    def __init__(self, initial_dict: Optional[Dict[Any, Any]] = None) -> None:
        self.lock = threading.Lock()
        self.internal = initial_dict or {}

    def set(self, key: Any, value: Any) -> None:
        with self.lock:
            self.internal[key] = value

    def get(self, key: Any, default: Any = None) -> Any:
        with self.lock:
            return self.internal.get(key, default)

    def pop(self, key: Any) -> Any:
        with self.lock:
            return self.internal.pop(key, None)

    def get_and_clear(self) -> Dict[Any, Any]:
        with self.lock:
            contents = self.internal.copy()
            self.internal.clear()
            return contents

    def __len__(self) -> int:
        return len(self.internal)

    def drain(self) -> Dict[Any, Any]:
        with self.lock:
            copy = self.internal.copy()
            self.internal.clear()
            return copy


class EulithWebsocketProvider(JSONBaseProvider):
    send_queue: queue.Queue[Tuple[Dict[Any, Any], Any]]
    termination_exception: Optional[Exception]

    def __init__(
        self,
        uri: str,
        bearer_token: str,
        thread_pool_workers: int = 10,
        max_reconnect_attempts: int = 10,
    ) -> None:
        super().__init__()

        self.uri = uri
        self.connection = None
        self.thread_pool = ThreadPoolExecutor(
            max_workers=thread_pool_workers, thread_name_prefix="eulith_ws_worker"
        )
        self.send_queue = queue.Queue()
        self.lock = threading.Lock()
        self.shutdown_event = threading.Event()
        self.termination_exception = None

        self.bearer = bearer_token
        self.request_id = 23428

        self.active_subscriptions = ThreadSafeDict()
        self.awaiting_one_time_response = ThreadSafeDict()
        self.awaiting_subscription_id = ThreadSafeDict()
        self.awaiting_unsubscribe = ThreadSafeDict()

        self.max_reconnect_attempts = max_reconnect_attempts

        self.main_thread = threading.Thread(target=self.run)
        self.main_thread.start()

    def run(self) -> None:
        while not self.shutdown_event.is_set():
            try:
                to_reestablish = self.active_subscriptions.get_and_clear()

                connection = self.connect()

                send_thread = threading.Thread(
                    target=self.send_loop, args=(connection,)
                )
                recv_thread = threading.Thread(
                    target=self.receive_loop, args=(connection,)
                )

                send_thread.start()
                recv_thread.start()

                self.reestablish_subscriptions(to_reestablish)

                send_thread.join()
                recv_thread.join()

                connection.close()
            except websocket.WebSocketConnectionClosedException:
                continue
            except CouldNotConnectException as ce:
                logger.error(f"Could not connect after retrying {ce}")
                self.terminate()
            except Exception as e:
                logger.error(f"Something unexpected happened: {e}")
                self.termination_exception = e
                self.terminate()

    def connect(self) -> Any:
        bearer_header = {"Authorization": f"Bearer {self.bearer}"}

        sleep = 1
        attempts = 0

        while attempts < self.max_reconnect_attempts:
            try:
                return websocket.create_connection(
                    self.uri, header=bearer_header, suppress_origin=True
                )
            except ConnectionRefusedError:
                time.sleep(random.uniform(0, sleep))
                sleep *= 2
                attempts += 1

        raise CouldNotConnectException()

    def reestablish_subscriptions(self, to_reestablish: Dict[Any, Any]) -> None:
        for key, val in to_reestablish.items():
            resubscribe_payload = val.get_resubscribe_payload()
            if resubscribe_payload:
                request_id = self.next_request_id()
                resubscribe_payload["id"] = request_id
                self.send_queue.put((resubscribe_payload, None))
                self.awaiting_subscription_id.set(request_id, val)

    def send_loop(self, connection: Any) -> None:
        """
        Runs on its own thread
        """
        while not self.shutdown_event.is_set():
            try:
                request, response_handler = self.send_queue.get(timeout=1)
                request_id = request.get("id")

                if response_handler:
                    self.awaiting_one_time_response.set(request_id, response_handler)

                connection.send(json.dumps(request))
            except queue.Empty:
                continue  # timeout after 1 second to check the shutdown event
            except Exception as e:
                logger.error(f"caught exception in eulith websocket send loop: {e}")
                return

        connection.close()

    def receive_loop(self, connection: Any) -> None:
        """
        Runs on its own thread
        """
        while not self.shutdown_event.is_set():
            try:
                message = connection.recv()

                try:
                    response_data = json.loads(message)
                except JSONDecodeError:
                    return  # This should only happen on socket shutdown when the close frame is received

                request_id = response_data.get("id", None)
                if request_id:
                    response_handler = self.awaiting_one_time_response.pop(request_id)
                    if response_handler:
                        response_handler.set_value(response_data)

                    # there's currently no case where we would pass back an error and a subscription ID
                    # should we pass subscription ID back if there's an error after a subscription is established?
                    if "error" in response_data and not response_handler:
                        sub_details = self.awaiting_subscription_id.pop(request_id)
                        if sub_details:
                            self.thread_pool.submit(
                                sub_details.handle_error, response_data
                            )
                            continue

                    sub_id = self.awaiting_unsubscribe.get(request_id, None)
                    if sub_id:
                        status = response_data.get("result", False)
                        if status:
                            self.active_subscriptions.pop(sub_id)
                            self.awaiting_unsubscribe.pop(request_id)
                        continue

                result = response_data.get("result", None)
                if isinstance(result, str):
                    subscription_id = result
                else:
                    params = response_data.get("params", {})
                    subscription_id = params.get("subscription", None)

                sub_details = self.awaiting_subscription_id.pop(request_id)
                if sub_details and subscription_id:
                    sub_details.set_subscription_id(subscription_id)
                    self.active_subscriptions.set(subscription_id, sub_details)

                sub_details = self.active_subscriptions.get(subscription_id)
                if sub_details:
                    self.thread_pool.submit(sub_details.handle_message, response_data)
            except Exception as e:
                logger.error(f"caught exception in eulith websocket receive loop: {e}")
                return

    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        if self.shutdown_event.is_set():
            raise CouldNotConnectException()

        response_handler = EulithSyncResponse()
        request_payload = self.get_request_payload(method, params)
        self.send_queue.put((request_payload, response_handler))
        return response_handler.get_value()

    def next_request_id(self) -> int:
        with self.lock:
            self.request_id += 1
            return self.request_id

    def terminate(self) -> None:
        self.shutdown_event.set()
        self.thread_pool.shutdown(False)
        self.drain_queue()
        self.drain_handlers()

    def drain_queue(self) -> None:
        done = 0
        while done == 0:
            try:
                request, response_handler = self.send_queue.get(timeout=1)
                if response_handler:
                    if self.termination_exception is not None:
                        response_handler.set_error(self.termination_exception)
                    else:
                        response_handler.set_error(CouldNotConnectException())
            except queue.Empty:
                done = 1

    def drain_handlers(self) -> None:
        for (
            request_id,
            response_handler,
        ) in self.awaiting_one_time_response.drain().items():
            if self.termination_exception is not None:
                response_handler.set_error(self.termination_exception)
            else:
                response_handler.set_error(CouldNotConnectException())

    def restart(self) -> None:
        # This method is only used in CI to test connection going up and down
        self.shutdown_event.clear()
        self.main_thread = threading.Thread(target=self.run)
        self.main_thread.start()
        self.thread_pool = ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="eulith_ws_worker"
        )

    def get_unsubscribe_message(self, subscription_id: str) -> Dict[str, Any]:
        rid = self.next_request_id()
        unsub_payload = {
            "jsonrpc": "2.0",
            "method": "eth_unsubscribe",
            "params": [subscription_id],
            "id": rid,
        }
        return unsub_payload

    def get_request_payload(
        self, method: RPCEndpoint, params: Any, rid: Optional[int] = None
    ) -> Dict[str, Any]:
        if not rid:
            rid = self.next_request_id()

        return {"id": rid, "method": str(method), "params": params, "jsonrpc": "2.0"}

    def subscribe(
        self,
        subscription_request: SubscribeRequest,
        handler: EulithWebsocketRequestHandler,
    ) -> SubscriptionHandle:
        subscription_type = subscription_request.get("subscription_type", None)
        method = (
            "eulith_subscribe"
            if subscription_type in EULITH_SUBSCRIPTION_TYPES
            else "eth_subscribe"
        )

        params: List[Any]
        if method == "eulith_subscribe":
            args = subscription_request.get("args", None)

            sub_type_body: Any
            if args:
                sub_type_body = {subscription_type: args}
            else:
                sub_type_body = subscription_type

            params = [
                {
                    "subscription_type": sub_type_body,
                }
            ]
        else:
            params = cast(List[Any], subscription_request.get("args", []))

        request_message = self.get_request_payload(RPCEndpoint(method), params)
        rid = request_message.get("id")

        sub_details = SubscriptionDetails(handler, request_message)
        self.awaiting_subscription_id.set(rid, sub_details)
        self.send_queue.put((request_message, None))

        return SubscriptionHandle(sub_details, self)

    def unsubscribe(self, sub_details: SubscriptionDetails) -> bool:
        if not sub_details.subscription_id:
            raise ValueError("subscription_id is missing")

        unsub_payload = self.get_unsubscribe_message(sub_details.subscription_id)
        unsub_response = EulithSyncResponse()

        request_id = unsub_payload.get("id", None)
        if not request_id:
            return False

        self.awaiting_unsubscribe.set(request_id, sub_details.subscription_id)
        self.send_queue.put((unsub_payload, unsub_response))

        response = unsub_response.get_value()
        return response.get("result", False)
