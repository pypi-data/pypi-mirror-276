from dataclasses import dataclass
from typing import Any, Dict

from eth_account.messages import encode_typed_data
from eth_utils import keccak

from eulith_web3.eip712_types import Eip712Data, Eip712Domain, Eip712Field


@dataclass
class HyperliquidCreateOrderHashInput:
    coin: str
    is_buy: bool
    size: str
    limit_price: str
    time_in_force: str
    reduce_only: bool
    vault_address: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "HyperliquidCreateOrderHashInput":
        return cls(
            coin=data["coin"],
            is_buy=data["is_buy"],
            size=data["size"],
            limit_price=data["limit_price"],
            time_in_force=data["time_in_force"],
            reduce_only=data["reduce_only"],
            vault_address=data["vault_address"],
        )

    def to_json(self) -> Dict[str, Any]:
        return dict(
            coin=self.coin,
            is_buy=self.is_buy,
            size=self.size,
            limit_price=self.limit_price,
            time_in_force=self.time_in_force,
            reduce_only=self.reduce_only,
            vault_address=self.vault_address,
        )


def get_hyper_liquid_create_order_typed_data(
    message: HyperliquidCreateOrderHashInput,
) -> Eip712Data:
    types = {
        "EIP712Domain": [
            Eip712Field(name="name", type="string"),
            Eip712Field(name="version", type="string"),
        ],
        "HyperliquidCreateOrderHashInput": [
            Eip712Field(name="coin", type="string"),
            Eip712Field(name="isBuy", type="bool"),
            Eip712Field(name="size", type="string"),
            Eip712Field(name="limitPrice", type="string"),
            Eip712Field(name="timeInForce", type="string"),
            Eip712Field(name="reduceOnly", type="bool"),
            Eip712Field(name="vaultAddress", type="string"),
        ],
    }

    payload = Eip712Data(
        types=types,
        primaryType="HyperliquidCreateOrderHashInput",
        domain={"name": "EulithAceHyperliquid", "version": "1"},
        message={
            "coin": message.coin,
            "isBuy": message.is_buy,
            "size": message.size,
            "limitPrice": message.limit_price,
            "timeInForce": message.time_in_force,
            "reduceOnly": message.reduce_only,
            "vaultAddress": message.vault_address,
        },
    )

    return payload


def get_hyper_liquid_create_order_hash(
    message: HyperliquidCreateOrderHashInput,
) -> bytes:
    signable_message = encode_typed_data(
        full_message=dict(get_hyper_liquid_create_order_typed_data(message))
    )
    return keccak(b"\x19\x01" + signable_message.header + signable_message.body)


@dataclass
class HyperliquidCancelOrderHashInput:
    coin: str
    oid: str
    vault_address: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "HyperliquidCancelOrderHashInput":
        return cls(
            coin=data["coin"], oid=data["oid"], vault_address=data["vault_address"]
        )

    def to_json(self) -> Dict[str, Any]:
        return dict(coin=self.coin, oid=self.oid, vault_address=self.vault_address)


def get_hyper_liquid_cancel_order_typed_data(
    message: HyperliquidCancelOrderHashInput,
) -> Eip712Data:
    types = {
        "EIP712Domain": [
            Eip712Field(name="name", type="string"),
            Eip712Field(name="version", type="string"),
        ],
        "HyperliquidCancelOrderHashInput": [
            Eip712Field(name="coin", type="string"),
            Eip712Field(name="oid", type="string"),
            Eip712Field(name="vaultAddress", type="string"),
        ],
    }

    payload = Eip712Data(
        types=types,
        primaryType="HyperliquidCancelOrderHashInput",
        domain=Eip712Domain(name="EulithAceHyperliquid", version="1"),
        message={
            "coin": message.coin,
            "oid": message.oid,
            "vaultAddress": message.vault_address,
        },
    )

    return payload


def get_hyper_liquid_cancel_order_hash(
    message: HyperliquidCancelOrderHashInput,
) -> bytes:
    signable_message = encode_typed_data(
        full_message=dict(get_hyper_liquid_cancel_order_typed_data(message))
    )
    return keccak(b"\x19\x01" + signable_message.header + signable_message.body)
