from typing import TypedDict, Optional


class DydxV3GetAceManagedAccountsRequest(TypedDict):
    ace_address: str  # Your ACE has a trading key it uses to sign txs, this is the address of that key


class DydxV3AceManagedAccountDetails(TypedDict):
    stark_public_key: str
    position_id: str
    equity: str
    free_collateral: str
    pending_deposits: str
    pending_withdrawals: str
    account_number: str
    quote_balance: str


class DydxV3AceManagedAccount(TypedDict):
    account_name: str
    account_details: DydxV3AceManagedAccountDetails


class DydxV3CreateOrderResponseInternal(TypedDict):
    id: str
    client_id: str
    account_id: str
    market: str
    side: str
    price: str
    trigger_price: str
    trailing_percent: str
    size: str
    remaining_size: str
    order_type: str
    created_at: str
    unfillable_at: Optional[str]
    expires_at: str
    status: str
    time_in_force: str
    post_only: bool
    reduce_only: bool
    cancel_reason: Optional[str]


class DydxV3CreateOrderResponse(TypedDict):
    order: DydxV3CreateOrderResponseInternal


class DyDxV3CreateOrderParams(TypedDict):
    market: str
    side: str
    order_type: str
    post_only: bool
    reduce_only: Optional[bool]
    size: str
    price: str
    limit_fee: str
    expiration: str
    time_in_force: Optional[str]
    trigger_price: Optional[str]
    trailing_percent: Optional[str]
    account_name: str
