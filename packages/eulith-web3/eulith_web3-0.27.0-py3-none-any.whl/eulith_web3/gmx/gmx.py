from typing import Any

from eulith_web3.gmx.v1.v1 import GmxV1Client
from eulith_web3.gmx.v2.v2 import GmxV2Client


class GMXClient:
    """
    A class that provides access to the GMX protocol.
    """

    # ew3 is an instance of EulithWeb3, but it's impossible to type with mypy because GMXClient and EulithWeb3 are
    # recursively linked to each other
    def __init__(self, ew3: Any) -> None:
        self.v2 = GmxV2Client(ew3.eulith_service)
        self.v1 = GmxV1Client(ew3)
