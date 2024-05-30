from typing import Any, Optional, Union, List, Tuple, TypedDict
from eth_typing import Address, ChecksumAddress
from web3 import Web3
from web3.types import TxParams
from .swap_data import SwapData
from .token_input import TokenInput
from .approx_params import ApproxParams
from .token_output import TokenOutput


def serialize_struct(d) -> tuple:
    if isinstance(d, dict):
        return tuple(serialize_struct(v) for v in d.values())
    elif isinstance(d, (list, tuple)):
        return tuple(serialize_struct(x) for x in d)
    else:
        return d


class ContractAddressNotSet(Exception):
    pass


class IPActionAddRemoveLiq:
    def __init__(
        self,
        web3: Web3,
        contract_address: Optional[Union[Address, ChecksumAddress]] = None,
    ):
        self.address: Optional[Union[Address, ChecksumAddress]] = contract_address
        self.abi = [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netSyUsed",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netPtUsed",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpOut",
                        "type": "uint256",
                    },
                ],
                "name": "AddLiquidityDualSyAndPt",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "tokenIn",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netTokenUsed",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netPtUsed",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpOut",
                        "type": "uint256",
                    },
                ],
                "name": "AddLiquidityDualTokenAndPt",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netPtIn",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpOut",
                        "type": "uint256",
                    },
                ],
                "name": "AddLiquiditySinglePt",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netSyIn",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpOut",
                        "type": "uint256",
                    },
                ],
                "name": "AddLiquiditySingleSy",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netSyIn",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpOut",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netYtOut",
                        "type": "uint256",
                    },
                ],
                "name": "AddLiquiditySingleSyKeepYt",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "token",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netTokenIn",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpOut",
                        "type": "uint256",
                    },
                ],
                "name": "AddLiquiditySingleToken",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "token",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netTokenIn",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpOut",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netYtOut",
                        "type": "uint256",
                    },
                ],
                "name": "AddLiquiditySingleTokenKeepYt",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netPtOut",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netSyOut",
                        "type": "uint256",
                    },
                ],
                "name": "RemoveLiquidityDualSyAndPt",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "tokenOut",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netPtOut",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netTokenOut",
                        "type": "uint256",
                    },
                ],
                "name": "RemoveLiquidityDualTokenAndPt",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netPtOut",
                        "type": "uint256",
                    },
                ],
                "name": "RemoveLiquiditySinglePt",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netSyOut",
                        "type": "uint256",
                    },
                ],
                "name": "RemoveLiquiditySingleSy",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "caller",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "market",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "token",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netTokenOut",
                        "type": "uint256",
                    },
                ],
                "name": "RemoveLiquiditySingleToken",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "netSyDesired",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "netPtDesired",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "minLpOut", "type": "uint256"},
                ],
                "name": "addLiquidityDualSyAndPt",
                "outputs": [
                    {"internalType": "uint256", "name": "netLpOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyUsed", "type": "uint256"},
                    {"internalType": "uint256", "name": "netPtUsed", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "tokenIn",
                                "type": "address",
                            },
                            {
                                "internalType": "uint256",
                                "name": "netTokenIn",
                                "type": "uint256",
                            },
                            {
                                "internalType": "address",
                                "name": "tokenMintSy",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "bulk",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "pendleSwap",
                                "type": "address",
                            },
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
                        "internalType": "struct TokenInput",
                        "name": "input",
                        "type": "tuple",
                    },
                    {
                        "internalType": "uint256",
                        "name": "netPtDesired",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "minLpOut", "type": "uint256"},
                ],
                "name": "addLiquidityDualTokenAndPt",
                "outputs": [
                    {"internalType": "uint256", "name": "netLpOut", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "netTokenUsed",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "netPtUsed", "type": "uint256"},
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "netPtIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minLpOut", "type": "uint256"},
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "guessMin",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "guessMax",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "guessOffchain",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "maxIteration",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "eps",
                                "type": "uint256",
                            },
                        ],
                        "internalType": "struct ApproxParams",
                        "name": "guessPtSwapToSy",
                        "type": "tuple",
                    },
                ],
                "name": "addLiquiditySinglePt",
                "outputs": [
                    {"internalType": "uint256", "name": "netLpOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "netSyIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minLpOut", "type": "uint256"},
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "guessMin",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "guessMax",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "guessOffchain",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "maxIteration",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "eps",
                                "type": "uint256",
                            },
                        ],
                        "internalType": "struct ApproxParams",
                        "name": "guessPtReceivedFromSy",
                        "type": "tuple",
                    },
                ],
                "name": "addLiquiditySingleSy",
                "outputs": [
                    {"internalType": "uint256", "name": "netLpOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "netSyIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minLpOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "minYtOut", "type": "uint256"},
                ],
                "name": "addLiquiditySingleSyKeepYt",
                "outputs": [
                    {"internalType": "uint256", "name": "netLpOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netYtOut", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "minLpOut", "type": "uint256"},
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "guessMin",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "guessMax",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "guessOffchain",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "maxIteration",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "eps",
                                "type": "uint256",
                            },
                        ],
                        "internalType": "struct ApproxParams",
                        "name": "guessPtReceivedFromSy",
                        "type": "tuple",
                    },
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "tokenIn",
                                "type": "address",
                            },
                            {
                                "internalType": "uint256",
                                "name": "netTokenIn",
                                "type": "uint256",
                            },
                            {
                                "internalType": "address",
                                "name": "tokenMintSy",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "bulk",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "pendleSwap",
                                "type": "address",
                            },
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
                        "internalType": "struct TokenInput",
                        "name": "input",
                        "type": "tuple",
                    },
                ],
                "name": "addLiquiditySingleToken",
                "outputs": [
                    {"internalType": "uint256", "name": "netLpOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "minLpOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "minYtOut", "type": "uint256"},
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "tokenIn",
                                "type": "address",
                            },
                            {
                                "internalType": "uint256",
                                "name": "netTokenIn",
                                "type": "uint256",
                            },
                            {
                                "internalType": "address",
                                "name": "tokenMintSy",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "bulk",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "pendleSwap",
                                "type": "address",
                            },
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
                        "internalType": "struct TokenInput",
                        "name": "input",
                        "type": "tuple",
                    },
                ],
                "name": "addLiquiditySingleTokenKeepYt",
                "outputs": [
                    {"internalType": "uint256", "name": "netLpOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netYtOut", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "minSyOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "minPtOut", "type": "uint256"},
                ],
                "name": "removeLiquidityDualSyAndPt",
                "outputs": [
                    {"internalType": "uint256", "name": "netSyOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netPtOut", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "tokenOut",
                                "type": "address",
                            },
                            {
                                "internalType": "uint256",
                                "name": "minTokenOut",
                                "type": "uint256",
                            },
                            {
                                "internalType": "address",
                                "name": "tokenRedeemSy",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "bulk",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "pendleSwap",
                                "type": "address",
                            },
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
                        "internalType": "struct TokenOutput",
                        "name": "output",
                        "type": "tuple",
                    },
                    {"internalType": "uint256", "name": "minPtOut", "type": "uint256"},
                ],
                "name": "removeLiquidityDualTokenAndPt",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "netTokenOut",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "netPtOut", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "minPtOut", "type": "uint256"},
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "guessMin",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "guessMax",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "guessOffchain",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "maxIteration",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "eps",
                                "type": "uint256",
                            },
                        ],
                        "internalType": "struct ApproxParams",
                        "name": "guessPtOut",
                        "type": "tuple",
                    },
                ],
                "name": "removeLiquiditySinglePt",
                "outputs": [
                    {"internalType": "uint256", "name": "netPtOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "minSyOut", "type": "uint256"},
                ],
                "name": "removeLiquiditySingleSy",
                "outputs": [
                    {"internalType": "uint256", "name": "netSyOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "netLpToRemove",
                        "type": "uint256",
                    },
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "tokenOut",
                                "type": "address",
                            },
                            {
                                "internalType": "uint256",
                                "name": "minTokenOut",
                                "type": "uint256",
                            },
                            {
                                "internalType": "address",
                                "name": "tokenRedeemSy",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "bulk",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "pendleSwap",
                                "type": "address",
                            },
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
                        "internalType": "struct TokenOutput",
                        "name": "output",
                        "type": "tuple",
                    },
                ],
                "name": "removeLiquiditySingleToken",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "netTokenOut",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
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

    def add_liquidity_dual_sy_and_pt(
        self,
        receiver: str,
        market: str,
        net_sy_desired: int,
        net_pt_desired: int,
        min_lp_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.addLiquidityDualSyAndPt(
            receiver, market, net_sy_desired, net_pt_desired, min_lp_out
        ).build_transaction(override_tx_parameters)

    def add_liquidity_dual_token_and_pt(
        self,
        receiver: str,
        market: str,
        input: TokenInput,
        net_pt_desired: int,
        min_lp_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.addLiquidityDualTokenAndPt(
            receiver, market, serialize_struct(input), net_pt_desired, min_lp_out
        ).build_transaction(override_tx_parameters)

    def add_liquidity_single_pt(
        self,
        receiver: str,
        market: str,
        net_pt_in: int,
        min_lp_out: int,
        guess_pt_swap_to_sy: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.addLiquiditySinglePt(
            receiver,
            market,
            net_pt_in,
            min_lp_out,
            serialize_struct(guess_pt_swap_to_sy),
        ).build_transaction(override_tx_parameters)

    def add_liquidity_single_sy(
        self,
        receiver: str,
        market: str,
        net_sy_in: int,
        min_lp_out: int,
        guess_pt_received_from_sy: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.addLiquiditySingleSy(
            receiver,
            market,
            net_sy_in,
            min_lp_out,
            serialize_struct(guess_pt_received_from_sy),
        ).build_transaction(override_tx_parameters)

    def add_liquidity_single_sy_keep_yt(
        self,
        receiver: str,
        market: str,
        net_sy_in: int,
        min_lp_out: int,
        min_yt_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.addLiquiditySingleSyKeepYt(
            receiver, market, net_sy_in, min_lp_out, min_yt_out
        ).build_transaction(override_tx_parameters)

    def add_liquidity_single_token(
        self,
        receiver: str,
        market: str,
        min_lp_out: int,
        guess_pt_received_from_sy: ApproxParams,
        input: TokenInput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.addLiquiditySingleToken(
            receiver,
            market,
            min_lp_out,
            serialize_struct(guess_pt_received_from_sy),
            serialize_struct(input),
        ).build_transaction(override_tx_parameters)

    def add_liquidity_single_token_keep_yt(
        self,
        receiver: str,
        market: str,
        min_lp_out: int,
        min_yt_out: int,
        input: TokenInput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.addLiquiditySingleTokenKeepYt(
            receiver, market, min_lp_out, min_yt_out, serialize_struct(input)
        ).build_transaction(override_tx_parameters)

    def remove_liquidity_dual_sy_and_pt(
        self,
        receiver: str,
        market: str,
        net_lp_to_remove: int,
        min_sy_out: int,
        min_pt_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.removeLiquidityDualSyAndPt(
            receiver, market, net_lp_to_remove, min_sy_out, min_pt_out
        ).build_transaction(override_tx_parameters)

    def remove_liquidity_dual_token_and_pt(
        self,
        receiver: str,
        market: str,
        net_lp_to_remove: int,
        output: TokenOutput,
        min_pt_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.removeLiquidityDualTokenAndPt(
            receiver, market, net_lp_to_remove, serialize_struct(output), min_pt_out
        ).build_transaction(override_tx_parameters)

    def remove_liquidity_single_pt(
        self,
        receiver: str,
        market: str,
        net_lp_to_remove: int,
        min_pt_out: int,
        guess_pt_out: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.removeLiquiditySinglePt(
            receiver,
            market,
            net_lp_to_remove,
            min_pt_out,
            serialize_struct(guess_pt_out),
        ).build_transaction(override_tx_parameters)

    def remove_liquidity_single_sy(
        self,
        receiver: str,
        market: str,
        net_lp_to_remove: int,
        min_sy_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.removeLiquiditySingleSy(
            receiver, market, net_lp_to_remove, min_sy_out
        ).build_transaction(override_tx_parameters)

    def remove_liquidity_single_token(
        self,
        receiver: str,
        market: str,
        net_lp_to_remove: int,
        output: TokenOutput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.removeLiquiditySingleToken(
            receiver, market, net_lp_to_remove, serialize_struct(output)
        ).build_transaction(override_tx_parameters)
