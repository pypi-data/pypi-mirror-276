from typing import Any, Optional, Union, List, Tuple, TypedDict
from eth_typing import Address, ChecksumAddress
from web3 import Web3
from web3.types import TxParams


class ContractAddressNotSet(Exception):
    pass


class IPInterestManagerYT:
    def __init__(
        self,
        web3: Web3,
        contract_address: Optional[Union[Address, ChecksumAddress]] = None,
    ):
        self.address: Optional[Union[Address, ChecksumAddress]] = contract_address
        self.abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "user", "type": "address"}
                ],
                "name": "userInterest",
                "outputs": [
                    {
                        "internalType": "uint128",
                        "name": "lastPYIndex",
                        "type": "uint128",
                    },
                    {
                        "internalType": "uint128",
                        "name": "accruedInterest",
                        "type": "uint128",
                    },
                ],
                "stateMutability": "view",
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

    def user_interest(self, user: str) -> Tuple[int, int]:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.userInterest(user).call()
