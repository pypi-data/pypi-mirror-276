from typing import List, Optional, TypedDict

from eulith_web3.eip712_types import Eip712Data, Eip712Domain, Eip712Field


class ClientWhitelist(TypedDict):
    list_id: int
    sorted_addresses: List[str]
    is_draft: bool


class CurrentWhitelists(TypedDict):
    auth_address: str
    active: Optional[ClientWhitelist]
    draft: Optional[ClientWhitelist]


class ClientWhitelistHashInput(TypedDict):
    owner_address: str
    safe_address: str
    list_contents: List[str]
    sub: str
    network_id: int


class ClientWhitelistHash(TypedDict):
    hash_input: ClientWhitelistHashInput
    hash: str


class AcceptedEnableArmorSignature(TypedDict):
    signature: str
    owner_address: str


def get_client_whitelist_typed_data(message: ClientWhitelistHashInput) -> Eip712Data:
    types = {
        "EIP712Domain": [
            Eip712Field(name="name", type="string"),
            Eip712Field(name="version", type="string"),
        ],
        "ClientWhitelistHashInput": [
            Eip712Field(name="ownerAddress", type="string"),
            Eip712Field(name="safeAddress", type="string"),
            Eip712Field(name="listContents", type="string[]"),
            Eip712Field(name="sub", type="string"),
            Eip712Field(name="networkId", type="int32"),
        ],
    }

    payload = Eip712Data(
        types=types,
        primaryType="ClientWhitelistHashInput",
        domain=Eip712Domain(name="Eulith", version="1"),
        message={
            "ownerAddress": message["owner_address"],
            "safeAddress": message["safe_address"],
            "listContents": message["list_contents"],
            "sub": message["sub"],
            "networkId": message["network_id"],
        },
    )

    return payload
