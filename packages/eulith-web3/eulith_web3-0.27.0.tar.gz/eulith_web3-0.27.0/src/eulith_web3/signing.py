import logging
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Mapping,
    Optional,
    Tuple,
)

from cytoolz import dissoc  # type: ignore
from eth_account._utils.legacy_transactions import (
    serializable_unsigned_transaction_from_dict,
    UnsignedTransaction,
    Transaction,
    encode_transaction,
)
from eth_account._utils.signing import to_eth_v
from eth_account._utils.typed_transactions import TypedTransaction
from eth_account.datastructures import SignedTransaction
from eth_keys.backends import NativeECCBackend, BaseECCBackend
from eth_keys.datatypes import PrivateKey, Signature
from eth_utils.toolz import (
    compose,
)
from hexbytes import HexBytes
from web3._utils.method_formatters import (
    STANDARD_NORMALIZERS,
)
from web3._utils.rpc_abi import (
    TRANSACTION_PARAMS_ABIS,
    apply_abi_formatters_to_dict,
)
from web3._utils.transactions import (
    fill_nonce,
    fill_transaction_defaults,
)
from web3.types import (
    Middleware,
    RPCEndpoint,
    RPCResponse,
    TxParams,
)

from eulith_web3.signer import Signer

if TYPE_CHECKING:
    from web3 import Web3  # noqa: F401

logger = logging.getLogger(__name__)


class SigningException(Exception):
    pass


def format_transaction(transaction: TxParams) -> TxParams:
    """Format transaction so that it can be used correctly in the signing middleware.

    Converts bytes to hex strings and other types that can be passed to the underlying layers.
    Also has the effect of normalizing 'from' for easier comparisons.
    """
    return apply_abi_formatters_to_dict(
        STANDARD_NORMALIZERS, TRANSACTION_PARAMS_ABIS, transaction
    )


def normalize_s(s: int) -> int:
    """
    Eth expects signatures in canonical form to avoid replay attacks.

    :param s: Signature's s value
    :return:  Normalized s value
    """
    n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
    if s > n // 2:
        s = n - s
    return s


def recover_v(
    r: int, s: int, message_hash: bytes, address: str, backend: BaseECCBackend
) -> Signature:
    s = normalize_s(s)
    sig0 = Signature(vrs=(0, r, s), backend=backend)
    if (
        sig0.recover_public_key_from_msg_hash(message_hash).to_checksum_address()
        == address
    ):
        return sig0
    sig1 = Signature(vrs=(1, r, s), backend=backend)
    if (
        sig1.recover_public_key_from_msg_hash(message_hash).to_checksum_address()
        == address
    ):
        return sig1
    raise SigningException("Could not determine v")


# signer has two functions: address, sign_msg_hash
#    def sign_msg_hash(self, message_hash: bytes) -> 'Signature':
def sign_transaction(transaction_dict: Any, signer: Signer) -> SignedTransaction:
    if not isinstance(transaction_dict, Mapping):
        raise TypeError("transaction_dict must be dict-like, got %r" % transaction_dict)

    # allow from field, *only* if it matches the private key
    if "from" in transaction_dict:
        if transaction_dict["from"] == signer.address:
            sanitized_transaction = dissoc(transaction_dict, "from")
        else:
            raise TypeError(
                "from field must match key's %s, but it was %s"
                % (
                    signer.address,
                    transaction_dict["from"],
                )
            )
    else:
        sanitized_transaction = transaction_dict

    (v, r, s, encoded_transaction, transaction_hash) = sign_transaction_dict(
        signer, sanitized_transaction
    )

    return SignedTransaction(
        rawTransaction=HexBytes(encoded_transaction),
        hash=HexBytes(transaction_hash),
        r=r,
        s=s,
        v=v,
    )


def sign_transaction_dict(
    eth_key: Signer, transaction_dict: Any
) -> Tuple[int, int, int, Any, bytes]:
    # generate RLP-serializable transaction, with defaults filled
    unsigned_transaction = serializable_unsigned_transaction_from_dict(transaction_dict)
    transaction_hash = unsigned_transaction.hash()

    # detect chain
    if isinstance(unsigned_transaction, UnsignedTransaction):
        signature = eth_key.sign_transaction(unsigned_transaction, transaction_hash)
        (v_raw, r, s) = signature.vrs
        v = to_eth_v(v_raw, None)
    elif isinstance(unsigned_transaction, Transaction):
        chain_id = unsigned_transaction.v

        signature = eth_key.sign_transaction(unsigned_transaction, transaction_hash)
        (v_raw, r, s) = signature.vrs
        v = to_eth_v(v_raw, chain_id)
    elif isinstance(unsigned_transaction, TypedTransaction):
        # Each transaction type dictates its payload, and consequently,
        # all the funky logic around the `v` signature field is both obsolete &&
        # incorrect. We want to obtain the raw `v` and delegate
        # to the transaction type itself.
        (v, r, s) = eth_key.sign_transaction(unsigned_transaction, transaction_hash).vrs
    else:
        # Cannot happen, but better for code to be defensive + self-documenting.
        raise TypeError("unknown Transaction object: %s" % type(unsigned_transaction))

    # serialize transaction with rlp
    encoded_transaction = encode_transaction(unsigned_transaction, vrs=(v, r, s))

    return v, r, s, encoded_transaction, transaction_hash


class LocalSigner(Signer):
    def __init__(
        self, private_key: Any, backend: Optional[BaseECCBackend] = None
    ) -> None:
        self.private_key = PrivateKey(
            HexBytes(private_key), backend or NativeECCBackend()
        )
        self._address = self.private_key.public_key.to_checksum_address()

    @property
    def address(self) -> str:
        return self._address

    def sign_msg_hash(self, message_hash: bytes) -> Signature:
        return self.private_key.sign_msg_hash(message_hash)


@dataclass
class EulithSigningMiddleware:
    middleware: Middleware
    address: str
    signer: Signer


def construct_signing_middleware(account: Signer) -> EulithSigningMiddleware:
    """
    Wrap signature source in middleware to allow for automatic signing when necessary for transactions
    being signed and sent directly to the network (as opposed to an atomic transaction, which gets sent
    unsigned to the Eulith server).

    :param account: The LocalSigner, KMSSigner, or FireblocksSigner for your wallet
    :type account: Signer
    """
    acct = account

    def sign_and_send_raw_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], w3: "Web3"
    ) -> Callable[[RPCEndpoint, Any], RPCResponse]:
        format_and_fill_tx = compose(
            format_transaction, fill_transaction_defaults(w3), fill_nonce(w3)
        )

        def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
            if method != "eth_sendTransaction":
                return make_request(method, params)
            else:
                transaction = format_and_fill_tx(params[0])

            if "from" not in transaction:
                return make_request(method, params)
            elif transaction.get("from") != acct.address:
                return make_request(method, params)

            raw_tx = sign_transaction(transaction, acct).rawTransaction

            return make_request(RPCEndpoint("eth_sendRawTransaction"), [raw_tx])

        return middleware

    return EulithSigningMiddleware(
        middleware=sign_and_send_raw_middleware, address=account.address, signer=acct
    )


def normalize_signature(signature: Signature) -> str:
    """
    Normalize the signature to a string, for instance for serialization for an RPC method.
    """
    compatible_v = signature.v + 27
    last_two_chars = hex(compatible_v)[-2:]
    return str(signature)[:-2] + last_two_chars
