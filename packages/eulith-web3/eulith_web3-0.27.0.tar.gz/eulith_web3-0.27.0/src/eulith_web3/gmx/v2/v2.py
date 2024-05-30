from eulith_web3.eulith_service import EulithService, JsonDict
from eulith_web3.exceptions import EulithRpcException
from eulith_web3.gmx.v2.rpc import (
    GmxV2CreateOrderRequest,
    GmxV2CreateOrderResponse,
    GmxV2GetPositionsRequest,
    GmxV2GetPositionsResponse,
)

from eulith_web3.gmx.v2.rpc import (
    GmxV2GetMarketPoolDataResponse,
    GmxV2GetMarketPoolDataRequest,
    GmxV2CreateDepositRequest,
    GmxV2CreateDepositResponse,
)


class GmxV2Client:
    def __init__(self, eulith_service: EulithService) -> None:
        self.eulith_service = eulith_service

    def get_tickers(self) -> JsonDict:
        return self.eulith_service.get_gmx_v2_tickers()

    def get_funding_rates(self) -> JsonDict:
        return self.eulith_service.get_gmx_v2_funding_rates()

    def get_positions(self, account: str) -> GmxV2GetPositionsResponse:
        request = GmxV2GetPositionsRequest(account=account)
        return self.eulith_service.gmx_v2_get_positions(request)

    def create_order(self, order: GmxV2CreateOrderRequest) -> GmxV2CreateOrderResponse:
        return self.eulith_service.gmx_v2_create_order(order)

    def get_market_pool_data(
        self, req: GmxV2GetMarketPoolDataRequest
    ) -> GmxV2GetMarketPoolDataResponse:
        return self.eulith_service.gmx_v2_get_market_pool_data(req)

    def create_deposit(
        self, req: GmxV2CreateDepositRequest
    ) -> GmxV2CreateDepositResponse:
        return self.eulith_service.gmx_v2_create_deposit(req)
