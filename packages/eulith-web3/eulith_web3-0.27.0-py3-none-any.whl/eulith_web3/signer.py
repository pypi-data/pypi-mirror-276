from abc import ABC
from typing import Any, Dict, Union

from eth_account._utils.typed_transactions import TypedTransaction
from eth_keys.datatypes import Signature
from web3.types import TxParams

from eulith_web3.eip712_types import Eip712Data


class Signer(ABC):
    @property
    def address(self) -> str:
        raise NotImplementedError

    def sign_msg_hash(self, message_hash: bytes) -> Signature:
        raise NotImplementedError

    def sign_transaction(
        self, tx: Union[TxParams, TypedTransaction], message_hash: bytes
    ) -> Signature:
        return self.sign_msg_hash(message_hash)

    def sign_typed_data(
        self, eip712_data: Union[Eip712Data, Dict[str, Any]], message_hash: bytes
    ) -> Signature:
        return self.sign_msg_hash(message_hash)
