from typing import List, TypedDict


class AddressOnChain(TypedDict):
    address: str
    chain_id: int


class Whitelist(TypedDict):
    list_id: int
    display_name: str
    sorted_addresses: List[AddressOnChain]
    is_draft: bool


class Sublist(TypedDict):
    list_id: int
    name: str


class ActivateHashInput(TypedDict):
    activation_id: int
    list_id: int
    auth_address: str
    safe_address: str
    chain_id: int
    whitelisted_addresses: List[AddressOnChain]
    sublists: List[Sublist]
