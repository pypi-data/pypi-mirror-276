import urllib.parse
import uuid
from typing import Any, Optional, List, Dict, Tuple, Union

from eth_keys.datatypes import Signature
from eth_typing import URI, ChecksumAddress, HexStr
from web3.types import RPCResponse, RPCEndpoint, TxParams

from eulith_web3.gmx.v2.rpc import (
    GmxV2CreateOrderRequest,
    GmxV2CreateOrderResponse,
    GmxV2GetPositionsRequest,
    GmxV2GetPositionsResponse,
)

from eulith_web3.gmx.v2.rpc import (
    GmxV2GetMarketPoolDataRequest,
    GmxV2GetMarketPoolDataResponse,
    GmxV2CreateDepositRequest,
    GmxV2CreateDepositResponse,
)

from eulith_web3.hyperliquid.rpc import HyperliquidGetDataRequest

from eulith_web3.hyperliquid._eip712 import HyperliquidCreateOrderHashInput

from eulith_web3.hyperliquid.rpc import HyperliquidGetHistoricalFundingRequest

from eulith_web3.hyperliquid.rpc import HyperliquidGetHistoricalFundingResponse
from eulith_web3 import whitelists_v2
from eulith_web3.ace import AceImmediateTx, AcePingResponse
from eulith_web3.atomic import BundleRequest
from eulith_web3.dydx.v3.rpc import DydxV3AceManagedAccount, DyDxV3CreateOrderParams
from eulith_web3.erc20 import EulithERC20, TokenSymbol
from eulith_web3.exceptions import EulithRpcException
from eulith_web3.pendle import PendleMarketSymbol
from eulith_web3.requests import (
    EulithShortOnRequest,
    EulithShortOffRequest,
    EulithAaveV2StartLoanRequest,
)
from eulith_web3.response import raise_if_error
from eulith_web3.swap import (
    EulithSwapRequest,
    EulithSwapProvider,
    EulithLiquiditySource,
)
from eulith_web3.uniswap import (
    EulithUniV3StartLoanRequest,
    EulithUniV3StartSwapRequest,
    EulithUniV3SwapQuoteRequest,
    EulithUniswapPoolLookupRequest,
)
from eulith_web3.websocket import (
    EulithWebsocketProvider,
    SubscribeRequest,
    EulithWebsocketRequestHandler,
    SubscriptionHandle,
    ThreadSafeDict,
)
from eulith_web3.whitelists import AcceptedEnableArmorSignature


JsonDict = Dict[str, Any]


def ensure_formatted_ws_url(eulith_url: str) -> str:
    if eulith_url.startswith("http://"):
        return "ws" + eulith_url[4:]
    elif eulith_url.startswith("https://"):
        return "wss" + eulith_url[5:]
    return eulith_url


def get_headers(token: str) -> Dict[str, str]:
    """
    Function returns a dictionary of headers to be used in an HTTP request.

    :param token: The bearer token to be included in the Authorization header.

    :return: A dictionary of headers to be used in an HTTP request.

    Example:
        get_headers("https://www.exampletokenwebsite.com", "token123")
    Returns: {
        'Authorization': 'Bearer token123',
        'Content-Type': 'application/json'
    }
    """

    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}

    return headers


def add_params_to_url(url: str, params: JsonDict) -> str:
    """
    This function takes in a URL and a dictionary of parameters and adds the parameters to the URL as query parameters.
    Eulith relies on query params to specify your atomic tx id or gnosis safe address, for example.

    :param url: The URL to which the parameters will be added.
    :param params: The dictionary of parameters that will be added to the URL.

    :return: The URL with the added parameters as query parameters.

    Example:
        add_params_to_url("https://www.example.com", {"param1": "value1", "param2": "value2"})
        Returns: "https://www.example.com?param1=value1&param2=value2"
    """

    url_parts = urllib.parse.urlparse(url)
    query = dict(urllib.parse.parse_qsl(url_parts.query))
    query.update(params)

    return url_parts._replace(query=urllib.parse.urlencode(query)).geturl()


class AtomicTxParams:
    def __init__(self, tx_id: str, safe_address: str, trading_key: str):
        self.tx_id = tx_id
        self.safe_address = safe_address
        self.trading_key = trading_key

    def inject_in_body(self, post_body: Dict[str, Any]) -> None:
        post_body.update({"auth_address": self.trading_key})

        if self.tx_id:
            post_body.update(
                {
                    "atomic_tx_id": self.tx_id,
                }
            )

        if self.safe_address:
            post_body.update({"gnosis_address": self.safe_address})


class EulithService:
    """
    Embedded class to represent data of the Eulith API and provides methods to interact with the API.

    :ivar eulith_url: URL of the Eulith API
    :ivar eulith_token: Refresh token for the Eulith API
    :ivar private: bool switches on whether transactions are routed through a private mempool or not
    :ivar atomic: Boolean indicating if the current transaction is atomic
    :ivar tx_id: ID of the current transaction
    :ivar eulith_provider: HTTP provider instance to make requests to the Eulith API
    """

    def __init__(
        self,
        eulith_url: str,
        eulith_token: str,
        private: bool = False,
        auth_address: Optional[str] = None,
    ) -> None:
        """
        :param eulith_url: URL of the Eulith API
        :param eulith_token: Refresh token for the Eulith API
        """

        self.token = eulith_token

        url_params = {}

        if private:
            url_params["private"] = "true"

        if auth_address:
            url_params["auth_address"] = auth_address

        self.eulith_url = URI(
            add_params_to_url(ensure_formatted_ws_url(eulith_url), url_params)
        )

        self.atomic_params: Optional[AtomicTxParams] = None
        self.headers = get_headers(self.token)

        self.eulith_provider = EulithWebsocketProvider(
            uri=self.eulith_url, bearer_token=self.token
        )

    def is_atomic(self) -> bool:
        if not self.atomic_params:
            return False

        return bool(self.atomic_params.tx_id)

    def server_version(self) -> str:
        return self._make_request("eulith_version", [])

    def send_transaction(self, params: Any) -> RPCResponse:
        """
        Sends a transaction to the blockchain via the Eulith RPC provider, handling exceptions that may occur
        when making a request with the make_request method from the HTTPProvider class.

        :param params: Dictionary containing the parameters for the transaction
        """

        params_list = list(params)

        if self.atomic_params and len(params_list) > 0:
            self.atomic_params.inject_in_body(params_list[0])

        # can't use self._make_request because we need to return the JSON-RPC object
        json_rpc = self.eulith_provider.make_request(
            RPCEndpoint("eth_sendTransaction"), params_list
        )
        raise_if_error(json_rpc)
        return json_rpc

    def create_new_contract(
        self,
        trading_key: str,
        contract_type: Optional[str] = None,
        deploy_new_safe: bool = True,
        seed: Optional[int] = None,
    ) -> JsonDict:
        params: JsonDict = {"authorized_address": trading_key}

        if contract_type:
            params["contract_type"] = contract_type

        if not deploy_new_safe:
            params["safe_already_exists"] = True

        if seed:
            params["seed"] = seed

        return self._make_request("eulith_new_contract", [params])

    def start_transaction(self, trading_key: str, safe_address: str) -> None:
        """
        Starts a Eulith atomic transaction. Anything transaction you send within an atomic transaction
        will get confirmed as a single unit. Everything operation in the unit will succeeds,
        or the whole transactions fails. The state of the blockchain is frozen while your atomic transaction
        is processing; there can't be any sandwiches, state changes, etc, in between your atomic operations.
        """

        self.atomic_params = AtomicTxParams(
            str(uuid.uuid4()), safe_address, trading_key
        )

    def commit(self) -> TxParams:
        """
        Serializes the current pending atomic tx into a single transactional unit, and returns
        the unsigned params. To get the atomic transaction on-chain, you need to sign these params
        and submit the transaction as a signed payload. The Eulith API handles this automatically for you.

        :returns: A dictionary containing the transaction parameters.
        """

        if not self.atomic_params:
            raise EulithRpcException("cannot commit outside atomic context")

        params: JsonDict = {}
        self.atomic_params.inject_in_body(params)
        self.atomic_params = None

        return self._make_request("eulith_commit", [params])

    def commit_for_ace(self) -> AceImmediateTx:
        """
        Variant of `commit` which returns a typed data payload rather than an unsigned transaction. The client should
        then sign the payload and send it back to the server via the `send_ace_transaction` method.

        Use this method when you are using an ACE server for signing rather than signing transactions directly from the
        Python client.

        :returns: The typed data to be signed by the client.
        """

        if not self.atomic_params:
            raise EulithRpcException("cannot commit outside atomic context")

        params: JsonDict = {}
        self.atomic_params.inject_in_body(params)
        self.atomic_params = None

        result = self._make_request("eulith_commit_for_ace", [params])
        return AceImmediateTx.from_json(result)

    def rollback(self) -> None:
        """
        Rollback here refers to discarding txs added to the atomic tx bundle during the call.
        """

        if not self.atomic_params:
            return

        params: JsonDict = {}
        self.atomic_params.inject_in_body(params)
        self.atomic_params = None

        self._make_request("eulith_discard_atomic_transactions", [params])

    def swap_quote(self, params: EulithSwapRequest) -> JsonDict:
        """
        Makes a request to the Eulith API to obtain a quote for a token swap. The returned quote is by default
        the best price across multiple DEX aggregators.
        """
        recipient: Optional[ChecksumAddress]
        route_through: Optional[EulithSwapProvider]
        slippage_tolerance: Optional[float]
        liquidity_source: Optional[EulithLiquiditySource]
        from_address: Optional[ChecksumAddress]

        sell_address = params["sell_token"].address
        buy_address = params["buy_token"].address
        parsed_params: JsonDict = {
            "sell_token": sell_address,
            "buy_token": buy_address,
            "sell_amount": params.get("sell_amount"),
        }
        recipient = params.get("recipient", None)
        route_through = params.get("route_through", None)
        liquidity_source = params.get("liquidity_source", None)
        slippage_tolerance = params.get("slippage_tolerance", None)
        from_address = params.get("from_address", None)

        if recipient:
            parsed_params["recipient"] = recipient
        if route_through:
            parsed_params["route_through"] = route_through
        if liquidity_source:
            parsed_params["liquidity_source"] = liquidity_source
        if slippage_tolerance:
            parsed_params["slippage_tolerance"] = slippage_tolerance
        if from_address:
            parsed_params["from_address"] = from_address

        if self.atomic_params:
            rpc_method = "eulith_swap_atomic"
            self.atomic_params.inject_in_body(parsed_params)
        else:
            rpc_method = "eulith_swap"

        return self._make_request(rpc_method, [parsed_params])

    def short_on(self, params: EulithShortOnRequest) -> JsonDict:
        """
        Request the Eulith API to open a levered short position on a token.

        :param params: Request params
        :type params: EulithShortOnRequest
            collateral_token (EulithERC20) -- ERC20 token to be used as collateral.
            short_token (EulithERC20) -- ERC20 token to be shorted.
            collateral_amount (float) -- A float representing the amount of the `collateral_token` to be used.
        """
        # Extract the addresses of the collateral and short tokens from the `params` argument.
        collateral_address = params["collateral_token"].address
        short_address = params["short_token"].address

        # Create a dictionary of parameters for the request with the token addresses and collateral amount.
        parsed_params = {
            "collateral_token": collateral_address,
            "short_token": short_address,
            "collateral_amount": params.get("collateral_amount"),
        }

        if self.atomic_params:
            self.atomic_params.inject_in_body(parsed_params)
        else:
            raise EulithRpcException(
                "cannot call short on outside of an atomic context"
            )

        return self._make_request("eulith_short_on", [parsed_params])

    def short_off(self, params: EulithShortOffRequest) -> JsonDict:
        """
        Makes a request to the Eulith API to unwind an existing short.
        """

        collateral_address = params["collateral_token"].address
        short_address = params["short_token"].address

        parsed_params = {
            "collateral_token": collateral_address,
            "short_token": short_address,
            "repay_short_amount": params.get("repay_short_amount"),
            "true_for_unwind_a": params.get("true_for_unwind_a", True),
        }

        if self.atomic_params:
            self.atomic_params.inject_in_body(parsed_params)
        else:
            raise EulithRpcException(
                "cannot call short on outside of an atomic context"
            )

        return self._make_request("eulith_short_off", [parsed_params])

    def start_uniswap_v3_loan(self, params: EulithUniV3StartLoanRequest) -> str:
        """
        Makes a request to start a loan in Uniswap V3. This loan is its own atomic structure, meaning
        after you start a loan you have immediate access to the borrow tokens. Transactions you send
        after starting the loan are included in the loan until you call finish_inner to close the loan and
        return one layer up in the nested atomic structure.

        Note that loans have to execute in an atomic transaction. You can't execute a loan on its own.

        :returns: the pool fee, as a hex string
        """

        borrow_token_a = params["borrow_token_a"].address
        borrow_amount_a = params.get("borrow_amount_a")
        borrow_token_b = params.get("borrow_token_b", None)
        borrow_amount_b = params.get("borrow_amount_b", None)
        pay_transfer_from = params.get("pay_transfer_from", None)
        recipient = params.get("recipient", None)

        parsed_params = {
            "borrow_token_a": borrow_token_a,
            "borrow_amount_a": borrow_amount_a,
        }

        if borrow_token_b:
            parsed_params["borrow_token_b"] = borrow_token_b.address
        if borrow_amount_b:
            parsed_params["borrow_amount_b"] = borrow_amount_b
        if pay_transfer_from:
            parsed_params["pay_transfer_from"] = pay_transfer_from
        if recipient:
            parsed_params["recipient"] = recipient

        if self.atomic_params:
            self.atomic_params.inject_in_body(parsed_params)
        else:
            raise EulithRpcException(
                "cannot call start_uniswap_v3_loan outside of an atomic context"
            )

        return self._make_request("eulith_start_uniswapv3_loan", [parsed_params])

    def start_uniswap_v3_swap(self, params: EulithUniV3StartSwapRequest) -> str:
        """
        Starting a uniswap V3 swap, a trade of one token for another on the Uniswap v3 protocol.

        This swap is its own atomic structure, meaning after you start a swap you have immediate access to the
        buy_tokens tokens. Transactions you send after starting the swap are included in the loan until you call
        finish_inner to close the swap and return one layer up in the nested atomic structure.

        :returns: the pool fee, as a hex string
        """

        sell_token = params["sell_token"].address
        amount = params.get("amount")
        pool_address = params.get("pool_address")
        fill_or_kill = params.get("fill_or_kill")
        sqrt_limit_price = params.get("sqrt_limit_price")
        recipient = params.get("recipient", None)
        pay_transfer_from = params.get("pay_transfer_from", None)

        parsed_params = {
            "sell_token": sell_token,
            "amount": amount,
            "pool_address": pool_address,
            "fill_or_kill": fill_or_kill,
            "sqrt_limit_price": sqrt_limit_price,
        }

        if recipient:
            parsed_params["recipient"] = recipient

        if pay_transfer_from:
            parsed_params["pay_transfer_from"] = pay_transfer_from

        if self.atomic_params:
            self.atomic_params.inject_in_body(parsed_params)
        else:
            raise EulithRpcException("must call in atomic context")

        return self._make_request("eulith_start_uniswapv3_swap", [parsed_params])

    def start_aave_v2_loan(self, params: EulithAaveV2StartLoanRequest) -> str:
        """
        Start a loan using the Aave V2 protocol

        :returns: the loan fee, as a hex string
        """

        tokens = params["tokens"]
        token_params = []
        for t in tokens:
            token_params.append(
                {
                    "token_address": t["token_address"].address,
                    "amount": t.get("amount"),
                }
            )

        parsed_params = {
            "tokens": token_params,
        }

        if self.atomic_params:
            self.atomic_params.inject_in_body(parsed_params)
        else:
            raise EulithRpcException("must call in atomic context")

        return self._make_request("eulith_start_aavev2_loan", [parsed_params])

    def finish_inner(self) -> str:
        """
        Uniswap & Aave flash loans and swaps are their own "sub atomic" structures. So when you start
        one of those actions, you have to finish it by calling this method. "Finishing" here means you close the
        transaction and append it to the outer atomic structure.

        :returns: number of transactions as a hex string
        """
        params: JsonDict = {}

        if self.atomic_params:
            self.atomic_params.inject_in_body(params)
        else:
            raise EulithRpcException("must call in atomic context")

        return self._make_request("eulith_finish_inner", [params])

    def uniswap_v3_quote(self, params: EulithUniV3SwapQuoteRequest) -> JsonDict:
        """
        Request a quote from Uniswap V3 for a swap between two tokens.
        """

        parsed_params = {
            "sell_token": params["sell_token"].address,
            "buy_token": params["buy_token"].address,
            "amount": params["amount"],
            "true_for_amount_in": params.get("true_for_amount_in", True),
        }

        fee = params.get("fee", None)
        if fee:
            parsed_params["fee"] = fee.value

        return self._make_request("eulith_uniswapv3_quote", [parsed_params])

    def lookup_univ3_pool(
        self, params: EulithUniswapPoolLookupRequest
    ) -> List[JsonDict]:
        """
        Looking up information about UniSwap V3 pools.
        """

        parsed_params = {
            "token_a": params["token_a"].address,
            "token_b": params["token_b"].address,
            "fee": params["fee"].value,
        }

        return self._make_request("eulith_uniswapv3_pool_lookup", [parsed_params])

    def lookup_token_symbol(self, symbol: TokenSymbol) -> Tuple[str, int]:
        """
        Look up token information by ERC20 symbol.

        :return: A tuple containing the contract address of the token and the number of decimals of the token.
        """

        parsed_res = self._make_request("eulith_erc_lookup", [{"symbol": symbol}])
        if len(parsed_res) != 1:
            raise EulithRpcException(
                f"unexpected response for {symbol} lookup, token isn't recognized"
            )

        return (
            parsed_res[0].get("contract_address"),
            parsed_res[0].get("decimals"),
        )

    def get_gmx_addresses(self) -> JsonDict:
        """
        Returns a dictionary of GMX contract addresses.
        """
        return self._make_request("eulith_gmx_address_lookup", [])

    def get_gmx_positions(
        self,
        wallet_address: ChecksumAddress,
        collateral_tokens: List[EulithERC20],
        index_tokens: List[EulithERC20],
        is_long: List[bool],
    ) -> JsonDict:
        """
        Get positions of the given wallet for a given set of collateral and index tokens and directions

        :param wallet_address: The address to get the positions of
        :param collateral_tokens: List of the collateral tokens the positions belong to
        :param index_tokens: List of the index tokens the positions belong to
        :param is_long: List of the direction of each position True is long False is short
        """
        collateral_addresses = []
        index_addresses = []

        for t in collateral_tokens:
            collateral_addresses.append(t.address)

        for t in index_tokens:
            index_addresses.append(t.address)

        params = {
            "wallet_address": wallet_address,
            "collateral_addresses": collateral_addresses,
            "index_addresses": index_addresses,
            "is_long": is_long,
        }

        return self._make_request("eulith_gmx_position_lookup", [params])

    def request_gmx_mint_glp(
        self, pay_token: EulithERC20, pay_amount: float, slippage: Optional[float]
    ) -> JsonDict:
        """
        Requests to mint GLP tokens by providing pay_token and pay_amount.
        Returns minimum GLP tokens to be minted, minimum USD value and transactions to be executed to take the position.
        We handle some of this logic server-side to keep the client light and simple.

        :param pay_token: The token to pay with
        :param pay_amount: The amount of pay_token to use
        :param slippage: The slippage tolerance as a percentage, defaults to None, in percentage units i.e. 0.01
        """
        params = {
            "pay_token_address": pay_token.address,
            "pay_amount": pay_amount,
        }

        if slippage:
            params["slippage"] = slippage

        return self._make_request("eulith_mint_and_stake_glp", [params])

    def get_pt_quote(
        self, buy_pt_amount: float, market_address: ChecksumAddress
    ) -> JsonDict:
        params = {
            "market_address": market_address,
            "exact_pt_out": buy_pt_amount,
        }

        return self._make_request("eulith_pendle_pt_quote", [params])

    def submit_new_armor_hash(
        self, tx_hash: str, existing_safe_address: Optional[ChecksumAddress] = None
    ) -> bool:
        params = {"tx_hash": tx_hash}

        if existing_safe_address:
            params["safe_address"] = existing_safe_address

        return self._make_request("eulith_submit_armor_hash", [params])

    def get_deployed_execution_contracts(self) -> List[JsonDict]:
        result = self._make_request("eulith_get_contracts", [])
        return result["contracts"]

    def submit_safe_signature(
        self,
        module_address: str,
        owner_address: str,
        signature: str,
        signed_hash: str,
        signature_type: str,
    ) -> bool:
        params = {
            "module_address": module_address,
            "owner_address": owner_address,
            "signature": str(signature),
            "signed_hash": signed_hash,
            "signature_type": signature_type,
        }

        return self._make_request("eulith_submit_enable_safe_signature", [params])

    def get_enable_safe_tx(
        self, auth_address: str, owner_threshold: int, owners: List[str]
    ) -> JsonDict:  # For new Safes
        params = {
            "auth_address": auth_address,
            "owner_threshold": owner_threshold,
            "owners": owners,
        }

        return self._make_request("eulith_get_setup_safe_tx", [params])

    def get_enable_module_tx(self, auth_address: str) -> JsonDict:  # For existing Safes
        params = {
            "auth_address": auth_address,
        }

        return self._make_request("eulith_get_enable_module_tx", [params])

    def submit_enable_safe_tx_hash(self, tx_hash: str, *, has_ace: bool) -> bool:
        params = {
            "tx_hash": tx_hash,
            "has_ace": has_ace,
        }

        return self._make_request("eulith_submit_setup_safe_hash", [params])

    def submit_enable_module_tx_hash(
        self, tx_hash: str, trading_key_address: str
    ) -> bool:
        params = {
            "tx_hash": tx_hash,
            "auth_address": trading_key_address,
        }

        return self._make_request("eulith_submit_enable_module_hash", [params])

    def create_draft_client_whitelist_v2(
        self, request: whitelists_v2.rpc.CreateRequest
    ) -> whitelists_v2.rpc.CreateResponse:
        return self._make_request("eulith_create_draft_client_whitelist_v2", [request])

    def append_to_draft_client_whitelist_v2(
        self, request: whitelists_v2.rpc.AppendRequest
    ) -> whitelists_v2.rpc.AppendResponse:
        return self._make_request(
            "eulith_append_to_draft_client_whitelist_v2", [request]
        )

    def publish_client_whitelist(
        self, request: whitelists_v2.rpc.PublishRequest
    ) -> whitelists_v2.rpc.PublishResponse:
        return self._make_request("eulith_publish_whitelist", [request])

    def start_activate_whitelist(
        self, request: whitelists_v2.rpc.StartActivateRequest
    ) -> whitelists_v2.rpc.StartActivateResponse:
        return self._make_request("eulith_start_activate_whitelist", [request])

    def submit_activate_whitelist_signature(
        self, request: whitelists_v2.rpc.SubmitActivateSignatureRequest
    ) -> whitelists_v2.rpc.SubmitActivateSignatureResponse:
        return self._make_request(
            "eulith_submit_activate_whitelist_signature", [request]
        )

    def get_whitelist_by_id(
        self, request: whitelists_v2.rpc.GetByIdRequest
    ) -> whitelists_v2.rpc.GetByIdResponse:
        return self._make_request("eulith_get_whitelist_by_id", [request])

    def delete_draft_client_whitelist_v2(
        self, request: whitelists_v2.rpc.DeleteRequest
    ) -> whitelists_v2.rpc.DeleteResponse:
        return self._make_request("eulith_delete_draft_client_whitelist_v2", [request])

    def propose_light_simulation(
        self, safe_address: str, chain_id: int, to_enable: bool
    ) -> JsonDict:
        params = dict(safe_address=safe_address, chain_id=chain_id, to_enable=to_enable)

        return self._make_request("eulith_propose_light_simulation", [params])

    def get_light_simulation_proposal_hash(self, proposal_id: int) -> JsonDict:
        params = dict(proposal_id=proposal_id)

        return self._make_request("eulith_get_light_simulation_proposal_hash", [params])

    def submit_light_simulation_signature(
        self, proposal_id: int, owner_address: str, signature: str, signed_hash: str
    ) -> JsonDict:
        params = dict(
            proposal_id=proposal_id,
            owner_address=owner_address,
            signature=signature,
            signed_hash=signed_hash,
        )

        return self._make_request(
            "eulith_submit_light_simulation_proposal_signature", [params]
        )

    def get_active_light_simulation_proposals(self) -> JsonDict:
        return self._make_request("eulith_get_active_light_simulation_proposals", [])

    def delete_light_simulation_proposal(self, proposal_id: int) -> JsonDict:
        params = dict(proposal_id=proposal_id)

        return self._make_request("eulith_delete_light_simulation_proposal", [params])

    def get_accepted_enable_armor_signatures(
        self, auth_address: str
    ) -> List[AcceptedEnableArmorSignature]:
        params = {
            "auth_address": auth_address,
        }

        return self._make_request("eulith_get_enable_module_sigs", [params])

    def dydx_v3_get_ace_managed_accounts(
        self, ace_address: str
    ) -> List[DydxV3AceManagedAccount]:
        params = {
            "ace_address": ace_address,
        }

        return self._make_request("eulith_dydx_v3_get_ace_managed_accounts", [params])

    def dydx_v3_create_order(
        self,
        order: DyDxV3CreateOrderParams,
        signature: Union[Signature, str],
        ace_address: str,
    ) -> JsonDict:
        params = {
            "ace_address": ace_address,
            "signature": str(signature),
            "order": order,
        }

        return self._make_request("eulith_dydx_v3_create_order", [params])

    def dydx_v3_get_for_account(
        self, ace_address: str, dydx_account_name: str, data: str
    ) -> JsonDict:
        params = {
            "ace_address": ace_address,
            "account_name": dydx_account_name,
            "data": data,
        }

        return self._make_request("eulith_dydx_v3_get_for_account", [params])

    def get_gmx_v2_tickers(self) -> JsonDict:
        return self._make_request("eulith_gmx_v2_ticker_lookup", [])

    def get_gmx_v2_funding_rates(self) -> JsonDict:
        return self._make_request("eulith_gmx_v2_funding_rate_lookup", [])

    def gmx_v2_get_positions(
        self, request: GmxV2GetPositionsRequest
    ) -> GmxV2GetPositionsResponse:
        return self._make_request("eulith_gmx_v2_get_positions", [request])

    def gmx_v2_create_order(
        self, request: GmxV2CreateOrderRequest
    ) -> GmxV2CreateOrderResponse:
        return self._make_request("eulith_gmx_v2_create_order", [request])

    def gmx_v2_get_market_pool_data(
        self, request: GmxV2GetMarketPoolDataRequest
    ) -> GmxV2GetMarketPoolDataResponse:
        return self._make_request("eulith_gmx_v2_get_market_pool_data", [request])

    def gmx_v2_create_deposit(
        self, request: GmxV2CreateDepositRequest
    ) -> GmxV2CreateDepositResponse:
        return self._make_request("eulith_gmx_v2_create_deposit", [request])

    def hyperliquid_get_data(self, request: HyperliquidGetDataRequest) -> JsonDict:
        return self._make_request("eulith_hyperliquid_get_data", [request])

    def hyperliquid_get_funding_rates(
        self, request: HyperliquidGetHistoricalFundingRequest
    ) -> HyperliquidGetHistoricalFundingResponse:
        return self._make_request("eulith_hyperliquid_get_funding_rates", [request])

    def hyperliquid_create_order(
        self,
        order_params: HyperliquidCreateOrderHashInput,
        signature: str,
        ace_address: str,
    ) -> JsonDict:
        params = {
            "create_order_instruction": order_params.to_json(),
            "signature": signature,
            "ace_address": ace_address,
        }

        return self._make_request("eulith_hyperliquid_create_order", [params])

    def hyperliquid_cancel_order(
        self,
        order_params: HyperliquidCreateOrderHashInput,
        signature: str,
        ace_address: str,
    ) -> JsonDict:
        params = {
            "cancel_order_instruction": order_params.to_json(),
            "signature": signature,
            "ace_address": ace_address,
        }

        return self._make_request("eulith_hyperliquid_cancel_order", [params])

    def ping_ace(self, auth_address: str) -> AcePingResponse:
        params = {
            "auth_address": auth_address,
        }

        return self._make_request("eulith_ping_ace", [params])

    def send_ace_transaction(
        self, signature: str, ace_immediate_tx: AceImmediateTx
    ) -> HexStr:
        params = {
            "signature": signature,
            "immediate_tx": ace_immediate_tx.to_json(),
        }

        return self._make_request("eulith_send_ace_transaction", [params])

    def pendle_swap(
        self,
        sell_token: Union[EulithERC20, PendleMarketSymbol],
        buy_token: Union[EulithERC20, PendleMarketSymbol],
        sell_amount: float,
        slippage: float,
        pendle_market: ChecksumAddress,
        recipient: Optional[ChecksumAddress] = None,
    ) -> JsonDict:
        sell_token_param = (
            sell_token.address
            if isinstance(sell_token, EulithERC20)
            else sell_token.value
        )
        buy_token_param = (
            buy_token.address if isinstance(buy_token, EulithERC20) else buy_token.value
        )

        params = {
            "sell_token": sell_token_param,
            "buy_token": buy_token_param,
            "sell_amount": sell_amount,
            "slippage_tolerance": slippage,
            "market": pendle_market,
        }

        if recipient:
            params["recipient"] = recipient

        if self.atomic_params:
            self.atomic_params.inject_in_body(params)

        return self._make_request("eulith_pendle_swap", [params])

    def tx_bundle(self, request: BundleRequest) -> TxParams:
        return self._make_request("eulith_tx_bundle", [request])

    def get_subscriptions(self) -> ThreadSafeDict:
        return self.eulith_provider.active_subscriptions

    def subscribe(
        self,
        subscription_request: SubscribeRequest,
        handler: EulithWebsocketRequestHandler,
    ) -> SubscriptionHandle:
        return self.eulith_provider.subscribe(subscription_request, handler)

    def terminate(self) -> None:
        self.eulith_provider.terminate()

    def _make_request(self, method: str, params: List[Any]) -> Any:
        json_rpc = self.eulith_provider.make_request(RPCEndpoint(method), params)
        raise_if_error(json_rpc)
        return json_rpc["result"]
