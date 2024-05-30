import re
from typing import Any, Dict, Optional, Union

from eth_account._utils.signing import to_standard_v
from eth_account._utils.typed_transactions import TypedTransaction
from eth_keys.backends import BaseECCBackend, NativeECCBackend
from eth_keys.datatypes import Signature
from web3.types import TxParams

from eulith_web3.eip712_types import Eip712Data
from eulith_web3.ledger_interface.account import get_ledger_accounts, get_signer_path
from eulith_web3.ledger_interface.comms import init_dongle
from eulith_web3.ledger_interface.exceptions import LedgerError
from eulith_web3.ledger_interface.messages import ledger_sign_typed_data
from eulith_web3.ledger_interface.objects import Type2Transaction, Type1Transaction
from eulith_web3.ledger_interface.transactions import ledger_sign_transaction
from eulith_web3.signer import Signer


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


class LedgerSigner(Signer):
    def __init__(
        self, account_index: int = 0, backend: Optional[BaseECCBackend] = None
    ):
        self.backend = backend or NativeECCBackend()
        try:
            self.account = get_ledger_accounts()[account_index]
            self.dongle = init_dongle()
            self.signer_path = get_signer_path(account_index)
        except LedgerError:
            print("Could not communicate with your Ledger. Is it asleep?")
            exit(1)

    @property
    def address(self) -> str:
        return self.account.address

    def sign_transaction(
        self, tx: Union[TxParams, TypedTransaction], message_hash: bytes
    ) -> Signature:
        formatted_tx = {}
        if isinstance(tx, TypedTransaction):
            tx_dict = tx.as_dict()
        else:
            tx_dict = dict(tx)

        tx_type = tx_dict.get("type", 2)  # default to EIP 1559

        tx_dict.pop("type")

        for k, v in tx_dict.items():
            formatted_tx[camel_to_snake(k)] = v

        if tx_type == 1:
            tx_to_sign = Type1Transaction(**formatted_tx)
        elif tx_type == 2:
            tx_to_sign = Type2Transaction(**formatted_tx)
        else:
            raise LedgerError(f"not sure how to sign transaction type: {tx_type}")

        signature = ledger_sign_transaction(
            tx_to_sign, dongle=self.dongle, sender_path=self.signer_path
        )

        v = signature.v
        r = signature.r
        s = signature.s

        return Signature(vrs=(v, r, s))

    def sign_typed_data(
        self, eip712_data: Union[Eip712Data, Dict[str, Any]], message_hash: bytes
    ) -> Signature:
        signature = ledger_sign_typed_data(
            eip712_data, dongle=self.dongle, sender_path=self.signer_path
        )
        return Signature(vrs=(to_standard_v(signature.v), signature.r, signature.s))
