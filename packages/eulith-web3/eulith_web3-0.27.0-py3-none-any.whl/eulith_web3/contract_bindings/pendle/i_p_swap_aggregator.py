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


class IPSwapAggregator:
    def __init__(
        self,
        web3: Web3,
        contract_address: Optional[Union[Address, ChecksumAddress]] = None,
    ):
        self.address: Optional[Union[Address, ChecksumAddress]] = contract_address
        self.abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "tokenIn", "type": "address"},
                    {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                    {
                        "components": [
                            {
                                "internalType": "enum SwapType",
                                "name": "swapType",
                                "type": "uint8",
                            },
                            {
                                "internalType": "address",
                                "name": "extRouter",
                                "type": "address",
                            },
                            {
                                "internalType": "bytes",
                                "name": "extCalldata",
                                "type": "bytes",
                            },
                            {
                                "internalType": "bool",
                                "name": "needScale",
                                "type": "bool",
                            },
                        ],
                        "internalType": "struct SwapData",
                        "name": "swapData",
                        "type": "tuple",
                    },
                ],
                "name": "swap",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function",
            }
        ]
        self.bytecode = ""
        self.w3 = web3

    def deploy(self):
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = contract.constructor().transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        self.address = tx_receipt.contractAddress

    def swap(
        self,
        token_in: str,
        amount_in: int,
        swap_data: SwapData,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swap(
            token_in, amount_in, serialize_struct(swap_data)
        ).build_transaction(override_tx_parameters)
