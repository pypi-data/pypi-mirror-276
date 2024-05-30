from eulith_web3.dydx.v3.v3 import DyDxV3
from eulith_web3.eulith_service import EulithService


class DyDx:
    def __init__(self, eulith_service: EulithService):
        self.v3 = DyDxV3(eulith_service)
