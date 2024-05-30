from typing import TypedDict

from eulith_web3.dydx.v3.rpc import DyDxV3CreateOrderParams


class DydxV3CreateOrderHashInput(TypedDict):
    market: str
    side: str
    order_type: str
    post_only: bool
    reduce_only: bool
    size: str
    price: str
    limit_fee: str
    expiration: str
    time_in_force: str
    trigger_price: str
    trailing_percent: str
    account_name: str


def parse_request_to_hash_input(
    order: DyDxV3CreateOrderParams,
) -> DydxV3CreateOrderHashInput:
    time_in_force = order.get("time_in_force")
    if not time_in_force:
        time_in_force = ""

    trigger_price = order.get("trigger_price")
    if not trigger_price:
        trigger_price = ""

    trailing_percent = order.get("trailing_percent")
    if not trailing_percent:
        trailing_percent = ""

    reduce_only = order.get("reduce_only")
    if not reduce_only:
        reduce_only = False

    return DydxV3CreateOrderHashInput(
        market=order.get("market", ""),
        side=order.get("side", ""),
        order_type=order.get("order_type", ""),
        post_only=order.get("post_only", False),
        reduce_only=reduce_only,
        size=order.get("size", ""),
        price=order.get("price", ""),
        limit_fee=order.get("limit_fee", ""),
        expiration=order.get("expiration", ""),
        account_name=order.get("account_name", ""),
        time_in_force=time_in_force,
        trigger_price=trigger_price,
        trailing_percent=trailing_percent,
    )
