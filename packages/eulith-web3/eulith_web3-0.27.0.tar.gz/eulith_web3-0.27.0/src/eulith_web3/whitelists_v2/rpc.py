from typing import List, TypedDict

from ._core import ActivateHashInput, AddressOnChain, Whitelist


class CreateRequest(TypedDict):
    display_name: str
    addresses: List[AddressOnChain]


class CreateResponse(TypedDict):
    list_id: int


class DeleteRequest(TypedDict):
    list_id: int


class DeleteResponse(TypedDict):
    deleted: Whitelist


class GetByIdRequest(TypedDict):
    list_id: int


class GetByIdResponse(TypedDict):
    whitelist: Whitelist


class AppendRequest(TypedDict):
    list_id: int
    addresses: List[AddressOnChain]


class AppendResponse(TypedDict):
    draft: Whitelist


class PublishRequest(TypedDict):
    list_id: int


class PublishResponse(TypedDict):
    published: Whitelist


class StartActivateRequest(TypedDict):
    list_id: int
    auth_address: str
    safe_address: str
    chain_id: int


class StartActivateResponse(TypedDict):
    activation_id: int
    hash_input: ActivateHashInput
    hash: str


class SubmitActivateSignatureRequest(TypedDict):
    activation_id: int
    signer_address: str
    signature: str
    hash: str


class SubmitActivateSignatureResponse(TypedDict):
    signature_count: int
    signature_threshold: int
