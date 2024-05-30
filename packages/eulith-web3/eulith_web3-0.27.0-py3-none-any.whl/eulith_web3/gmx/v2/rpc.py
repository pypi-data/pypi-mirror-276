from typing import TypedDict, Optional, List

from web3.types import TxParams


class GmxV2CreateOrderRequest(TypedDict):
    market: str
    account: str
    size_delta_usd_float: Optional[float]
    size_delta_usd_raw: Optional[int]
    collateral_delta_tokens_float: Optional[float]
    collateral_delta_tokens_raw: Optional[int]
    is_increase: bool
    collateral_token: str
    limit_price: Optional[float]
    slippage: Optional[float]
    is_long: bool


class GmxV2CreateOrderResponse(TypedDict):
    txs: List[TxParams]


class GmxV2GetPositionsRequest(TypedDict):
    account: str


class GmxV2PositionAmountsParsed(TypedDict):
    size_in_usd: float
    size_in_tokens: float
    collateral_amount: float


class GmxV2PositionAmountsRaw(TypedDict):
    size_in_usd: int
    size_in_tokens: int
    collateral_amount: int
    borrowing_factor: int
    funding_fee_amount_per_size: int
    long_token_claimable_funding_amount_per_size: int
    short_token_claimable_funding_amount_per_size: int


class GmxV2PositionFeesParsed(TypedDict):
    claimable_long_token_amount: float
    claimable_short_token_amount: float
    position_fee_factor: float
    borrowing_fee_usd: float
    borrowing_fee_amount: float
    protocol_fee_amount: float
    position_fee_amount: float
    total_cost_amount: float


class GmxV2PositionFeesRaw(TypedDict):
    funding_fee_amount: int
    claimable_long_token_amount: int
    claimable_short_token_amount: int
    latest_funding_fee_amount_per_size: int
    latest_long_token_claimable_funding_amount_per_size: int
    latest_short_token_claimable_funding_amount_per_size: int
    position_fee_factor: int
    borrowing_fee_usd: int
    borrowing_fee_amount: int
    protocol_fee_amount: int
    position_fee_amount: int
    total_cost_amount: int


class GmxV2Position(TypedDict):
    account: str
    market: str
    collateral_token: str
    position_amounts_raw: GmxV2PositionAmountsRaw
    position_amounts_parsed: GmxV2PositionAmountsParsed
    position_fees_raw: GmxV2PositionFeesRaw
    position_fees_parsed: GmxV2PositionFeesParsed
    close_execution_price_raw: int
    close_execution_price_parsed: float
    pnl_raw_usd: int
    pnl_parsed_usd: float
    pnl_after_price_impact_raw_usd: int
    pnl_after_price_impact_parsed_usd: float
    is_long: bool


class GmxV2GetPositionsResponse(TypedDict):
    positions: List[GmxV2Position]


class GmxV2GetMarketPoolDataRequest(TypedDict):
    market: str


class GmxV2MarketPoolData(TypedDict):
    pool_value: int
    long_pnl: int
    short_pnl: int
    net_pnl: int
    long_token_amount: int
    short_token_amount: int
    long_token_usd: int
    short_token_usd: int
    total_borrowing_fees: int
    borrowing_fee_pool_factor: int
    impact_pool_amount: int


class GmxV2GetMarketPoolDataResponseInternal(TypedDict):
    raw_data: GmxV2MarketPoolData
    raw_price_usd: int
    parsed_price_usd: float


class GmxV2GetMarketPoolDataPnlTypeData(TypedDict):
    pnl_type: str
    data: GmxV2GetMarketPoolDataResponseInternal


class GmxV2GetMarketPoolDataResponse(TypedDict):
    market: str
    market_statistics: List[GmxV2GetMarketPoolDataPnlTypeData]


class GmxV2CreateDepositRequest(TypedDict):
    market: str
    account: str
    long_amount_float: Optional[float]
    long_amount_raw: Optional[int]
    short_amount_float: Optional[float]
    short_amount_raw: Optional[int]
    slippage: Optional[float]


class GmxV2CreateDepositResponse(TypedDict):
    txs: List[TxParams]
