from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from eth_account.messages import encode_typed_data
from eth_utils import keccak

from eulith_web3.eip712_types import Eip712Data, Eip712Domain, Eip712Field


@dataclass
class AceImmediateTx:
    chain_id: int
    nonce: int
    max_priority_fee_per_gas: int
    max_fee_per_gas: int
    gas_limit: int
    data: bytes

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "AceImmediateTx":
        return cls(
            chain_id=data["chain_id"],
            nonce=int(data["nonce"], base=16),
            max_priority_fee_per_gas=int(data["max_priority_fee_per_gas"], base=16),
            max_fee_per_gas=int(data["max_fee_per_gas"], base=16),
            gas_limit=int(data["gas_limit"], base=16),
            data=bytes.fromhex(data["data"][2:]),
        )

    def to_json(self) -> Dict[str, Any]:
        return dict(
            chain_id=self.chain_id,
            nonce=hex(self.nonce),
            max_priority_fee_per_gas=hex(self.max_priority_fee_per_gas),
            max_fee_per_gas=hex(self.max_fee_per_gas),
            gas_limit=hex(self.gas_limit),
            data="0x" + self.data.hex(),
        )


class AcePingResponse(TypedDict):
    ping_time_millis: int
    auth_address: str
    ui_address: str


def get_ace_immediate_tx_typed_data(message: AceImmediateTx) -> Eip712Data:
    # Should match the EIP-712 definition in src/ace/immediate_tx.rs
    types = {
        "EIP712Domain": [
            Eip712Field(name="name", type="string"),
            Eip712Field(name="version", type="string"),
        ],
        "AceImmediateTx": [
            Eip712Field(name="chainId", type="int64"),
            Eip712Field(name="nonce", type="uint256"),
            Eip712Field(name="maxPriorityFeePerGas", type="uint256"),
            Eip712Field(name="maxFeePerGas", type="uint256"),
            Eip712Field(name="gasLimit", type="uint256"),
            Eip712Field(name="data", type="bytes"),
        ],
    }

    payload = Eip712Data(
        types=types,
        primaryType="AceImmediateTx",
        domain=Eip712Domain(name="EulithAceImmediateTx", version="1"),
        message={
            "chainId": message.chain_id,
            "nonce": message.nonce,
            "maxPriorityFeePerGas": message.max_priority_fee_per_gas,
            "maxFeePerGas": message.max_fee_per_gas,
            "gasLimit": message.gas_limit,
            "data": message.data,
        },
    )

    return payload


def get_ace_immediate_tx_hash(ace_immediate_tx: AceImmediateTx) -> bytes:
    signable_message = encode_typed_data(
        full_message=dict(get_ace_immediate_tx_typed_data(ace_immediate_tx))
    )
    return keccak(b"\x19\x01" + signable_message.header + signable_message.body)
