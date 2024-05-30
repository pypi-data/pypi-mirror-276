from typing import Any, Dict, List

from ._core import ActivateHashInput, AddressOnChain, Sublist
from eulith_web3.eip712_types import Eip712Data, Eip712Domain, Eip712Field


class AddressOnChainEip712:
    x: AddressOnChain

    def __init__(self, x: AddressOnChain) -> None:
        self.x = x

    @classmethod
    def type(cls) -> List[Eip712Field]:
        return [
            Eip712Field(name="address", type="address"),
            Eip712Field(name="chainId", type="int32"),
        ]

    @classmethod
    def type_name(cls) -> str:
        return "AddressOnChain"

    def typed_data(self) -> Eip712Data:
        types = {
            "EIP712Domain": eip712_domain_type(),
            self.type_name(): self.type(),
        }

        payload = Eip712Data(
            types=types,
            primaryType=self.type_name(),
            domain=eip712_domain(),
            message={
                "address": self.x["address"],
                "chainId": self.x["chain_id"],
            },
        )

        return payload


class SublistEip712:
    x: Sublist

    def __init__(self, x: Sublist) -> None:
        self.x = x

    @classmethod
    def type(cls) -> List[Eip712Field]:
        return [
            Eip712Field(name="listId", type="int32"),
            Eip712Field(name="name", type="string"),
        ]

    @classmethod
    def type_name(cls) -> str:
        return "Sublist"

    def typed_data(self) -> Eip712Data:
        types = {
            "EIP712Domain": eip712_domain_type(),
            self.type_name(): self.type(),
        }

        payload = Eip712Data(
            types=types,
            primaryType=self.type_name(),
            domain=eip712_domain(),
            message={
                "listId": self.x["list_id"],
                "name": self.x["name"],
            },
        )

        return payload


class ActivateHashInputEip712:
    x: ActivateHashInput

    def __init__(self, x: ActivateHashInput) -> None:
        self.x = x

    @classmethod
    def eip712_type(cls) -> List[Eip712Field]:
        return [
            Eip712Field(name="activationId", type="int32"),
            Eip712Field(name="listId", type="int32"),
            Eip712Field(name="authAddress", type="address"),
            Eip712Field(name="safeAddress", type="address"),
            Eip712Field(name="chainId", type="int32"),
            Eip712Field(name="whitelistedAddresses", type="AddressOnChain[]"),
            Eip712Field(name="sublists", type="Sublist[]"),
        ]

    @classmethod
    def eip712_type_name(cls) -> str:
        return "ActivateHashInput"

    def typed_data(self) -> Eip712Data:
        types = {
            "EIP712Domain": eip712_domain_type(),
            AddressOnChainEip712.type_name(): AddressOnChainEip712.type(),
            SublistEip712.type_name(): SublistEip712.type(),
            self.eip712_type_name(): self.eip712_type(),
        }

        payload = Eip712Data(
            types=types,
            primaryType=self.eip712_type_name(),
            domain=eip712_domain(),
            message={
                "activationId": self.x["activation_id"],
                "listId": self.x["list_id"],
                "authAddress": self.x["auth_address"],
                "safeAddress": self.x["safe_address"],
                "chainId": self.x["chain_id"],
                "whitelistedAddresses": [
                    {
                        "address": address_on_chain["address"],
                        "chainId": address_on_chain["chain_id"],
                    }
                    for address_on_chain in self.x["whitelisted_addresses"]
                ],
                "sublists": [
                    {"listId": sublist["list_id"], "name": sublist["name"]}
                    for sublist in self.x["sublists"]
                ],
            },
        )

        return payload


def eip712_domain() -> Eip712Domain:
    return Eip712Domain(name="EulithActivateWhitelist", version="1")


def eip712_domain_type() -> List[Eip712Field]:
    return [
        Eip712Field(name="name", type="string"),
        Eip712Field(name="version", type="string"),
    ]
