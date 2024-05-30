from typing import List

from eth_account.messages import encode_typed_data
from eth_utils import keccak

from eulith_web3.dydx.v3._eip712 import DydxV3CreateOrderHashInput
from eulith_web3.eip712_types import Eip712Data, Eip712Domain, Eip712Field


def eip712_domain() -> Eip712Domain:
    return Eip712Domain(name="EulithAceDydxV3", version="1")


def eip712_domain_type() -> List[Eip712Field]:
    return [
        Eip712Field(name="name", type="string"),
        Eip712Field(name="version", type="string"),
    ]


class CreateOrderHashInputEip712:
    x: DydxV3CreateOrderHashInput

    def __init__(self, x: DydxV3CreateOrderHashInput) -> None:
        self.x = x

    @classmethod
    def eip712_type(cls) -> List[Eip712Field]:
        return [
            Eip712Field(name="market", type="string"),
            Eip712Field(name="side", type="string"),
            Eip712Field(name="orderType", type="string"),
            Eip712Field(name="postOnly", type="bool"),
            Eip712Field(name="reduceOnly", type="bool"),
            Eip712Field(name="size", type="string"),
            Eip712Field(name="price", type="string"),
            Eip712Field(name="limitFee", type="string"),
            Eip712Field(name="expiration", type="string"),
            Eip712Field(name="timeInForce", type="string"),
            Eip712Field(name="triggerPrice", type="string"),
            Eip712Field(name="trailingPercent", type="string"),
            Eip712Field(name="accountName", type="string"),
        ]

    @classmethod
    def eip712_type_name(cls) -> str:
        return "DydxV3CreateOrderHashInput"

    def typed_data(self) -> Eip712Data:
        types = {
            "EIP712Domain": eip712_domain_type(),
            self.eip712_type_name(): self.eip712_type(),
        }

        payload = Eip712Data(
            types=types,
            primaryType=self.eip712_type_name(),
            domain=eip712_domain(),
            message={
                "market": self.x["market"],
                "side": self.x["side"],
                "orderType": self.x["order_type"],
                "postOnly": self.x["post_only"],
                "reduceOnly": self.x["reduce_only"],
                "size": self.x["size"],
                "price": self.x["price"],
                "limitFee": self.x["limit_fee"],
                "expiration": self.x["expiration"],
                "timeInForce": self.x["time_in_force"],
                "triggerPrice": self.x["trigger_price"],
                "trailingPercent": self.x["trailing_percent"],
                "accountName": self.x["account_name"],
            },
        )

        return payload

    def compute_hash(self) -> bytes:
        signable_message = encode_typed_data(full_message=dict(self.typed_data()))
        return keccak(b"\x19\x01" + signable_message.header + signable_message.body)
