from typing import Any, Dict, List, TypedDict


class Eip712Field(TypedDict):
    name: str
    type: str


class Eip712Domain(TypedDict, total=False):
    name: str
    version: str
    verifyingContract: str
    chainId: int


class Eip712Data(TypedDict):
    types: Dict[str, List[Eip712Field]]
    primaryType: str
    domain: Eip712Domain
    message: Dict[str, Any]
