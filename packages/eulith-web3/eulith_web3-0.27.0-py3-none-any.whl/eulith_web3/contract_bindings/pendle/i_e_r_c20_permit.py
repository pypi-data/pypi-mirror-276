from typing import Any, Optional, Union, List, Tuple, TypedDict
from eth_typing import Address, ChecksumAddress
from web3 import Web3
from web3.types import TxParams
from .swap_data import SwapData
from .token_input import TokenInput
from .approx_params import ApproxParams
from .token_output import TokenOutput
from .multi_approval import MultiApproval
from .call3 import Call3


def serialize_struct(d) -> tuple:
    if isinstance(d, dict):
        return tuple(serialize_struct(v) for v in d.values())
    elif isinstance(d, (list, tuple)):
        return tuple(serialize_struct(x) for x in d)
    else:
        return d


class ContractAddressNotSet(Exception):
    pass


class IERC20Permit:
    def __init__(
        self,
        web3: Web3,
        contract_address: Optional[Union[Address, ChecksumAddress]] = None,
    ):
        self.address: Optional[Union[Address, ChecksumAddress]] = contract_address
        self.abi = [
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ]
        self.bytecode = ""
        self.w3 = web3

    def deploy(self):
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = contract.constructor().transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        self.address = tx_receipt.contractAddress

    def d_o_m_a_i_n__s_e_p_a_r_a_t_o_r(self) -> bytes:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.DOMAIN_SEPARATOR().call()

    def nonces(self, owner: str) -> int:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.nonces(owner).call()

    def permit(
        self,
        owner: str,
        spender: str,
        value: int,
        deadline: int,
        v: int,
        r: bytes,
        s: bytes,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.permit(
            owner, spender, value, deadline, v, r, s
        ).build_transaction(override_tx_parameters)
