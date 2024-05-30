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


class IPAllAction:
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
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "YT",
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
                        "name": "netPyOut",
                        "type": "uint256",
                    },
                ],
                "name": "MintPyFromSy",
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
                        "name": "tokenIn",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "YT",
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
                        "name": "netPyOut",
                        "type": "uint256",
                    },
                ],
                "name": "MintPyFromToken",
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
                        "name": "tokenIn",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "SY",
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
                        "name": "netSyOut",
                        "type": "uint256",
                    },
                ],
                "name": "MintSyFromToken",
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
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "YT",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netPyIn",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netSyOut",
                        "type": "uint256",
                    },
                ],
                "name": "RedeemPyToSy",
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
                        "name": "tokenOut",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "YT",
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
                        "name": "netPyIn",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netTokenOut",
                        "type": "uint256",
                    },
                ],
                "name": "RedeemPyToToken",
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
                        "name": "tokenOut",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "SY",
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
                        "name": "netSyIn",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "netTokenOut",
                        "type": "uint256",
                    },
                ],
                "name": "RedeemSyToToken",
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
                        "internalType": "int256",
                        "name": "netPtToAccount",
                        "type": "int256",
                    },
                    {
                        "indexed": False,
                        "internalType": "int256",
                        "name": "netSyToAccount",
                        "type": "int256",
                    },
                ],
                "name": "SwapPtAndSy",
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
                        "internalType": "int256",
                        "name": "netPtToAccount",
                        "type": "int256",
                    },
                    {
                        "indexed": False,
                        "internalType": "int256",
                        "name": "netTokenToAccount",
                        "type": "int256",
                    },
                ],
                "name": "SwapPtAndToken",
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
                        "internalType": "int256",
                        "name": "netPtToAccount",
                        "type": "int256",
                    },
                    {
                        "indexed": False,
                        "internalType": "int256",
                        "name": "netYtToAccount",
                        "type": "int256",
                    },
                ],
                "name": "SwapPtAndYt",
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
                        "internalType": "int256",
                        "name": "netYtToAccount",
                        "type": "int256",
                    },
                    {
                        "indexed": False,
                        "internalType": "int256",
                        "name": "netSyToAccount",
                        "type": "int256",
                    },
                ],
                "name": "SwapYtAndSy",
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
                        "internalType": "int256",
                        "name": "netYtToAccount",
                        "type": "int256",
                    },
                    {
                        "indexed": False,
                        "internalType": "int256",
                        "name": "netTokenToAccount",
                        "type": "int256",
                    },
                ],
                "name": "SwapYtAndToken",
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
                    {
                        "components": [
                            {
                                "internalType": "address[]",
                                "name": "tokens",
                                "type": "address[]",
                            },
                            {
                                "internalType": "address",
                                "name": "spender",
                                "type": "address",
                            },
                        ],
                        "internalType": "struct IPActionMisc.MultiApproval[]",
                        "name": "",
                        "type": "tuple[]",
                    }
                ],
                "name": "approveInf",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "components": [
                            {
                                "internalType": "bool",
                                "name": "allowFailure",
                                "type": "bool",
                            },
                            {
                                "internalType": "bytes",
                                "name": "callData",
                                "type": "bytes",
                            },
                        ],
                        "internalType": "struct IPActionMisc.Call3[]",
                        "name": "calls",
                        "type": "tuple[]",
                    }
                ],
                "name": "batchExec",
                "outputs": [
                    {
                        "components": [
                            {"internalType": "bool", "name": "success", "type": "bool"},
                            {
                                "internalType": "bytes",
                                "name": "returnData",
                                "type": "bytes",
                            },
                        ],
                        "internalType": "struct IPActionMisc.Result[]",
                        "name": "returnData",
                        "type": "tuple[]",
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "bytes4",
                        "name": "_functionSelector",
                        "type": "bytes4",
                    }
                ],
                "name": "facetAddress",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "facetAddress_",
                        "type": "address",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "facetAddresses",
                "outputs": [
                    {
                        "internalType": "address[]",
                        "name": "facetAddresses_",
                        "type": "address[]",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "_facet", "type": "address"}
                ],
                "name": "facetFunctionSelectors",
                "outputs": [
                    {
                        "internalType": "bytes4[]",
                        "name": "facetFunctionSelectors_",
                        "type": "bytes4[]",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "facets",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "facetAddress",
                                "type": "address",
                            },
                            {
                                "internalType": "bytes4[]",
                                "name": "functionSelectors",
                                "type": "bytes4[]",
                            },
                        ],
                        "internalType": "struct IDiamondLoupe.Facet[]",
                        "name": "facets_",
                        "type": "tuple[]",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "YT", "type": "address"},
                    {"internalType": "uint256", "name": "netSyIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minPyOut", "type": "uint256"},
                ],
                "name": "mintPyFromSy",
                "outputs": [
                    {"internalType": "uint256", "name": "netPyOut", "type": "uint256"}
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "YT", "type": "address"},
                    {"internalType": "uint256", "name": "minPyOut", "type": "uint256"},
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
                "name": "mintPyFromToken",
                "outputs": [
                    {"internalType": "uint256", "name": "netPyOut", "type": "uint256"}
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "SY", "type": "address"},
                    {"internalType": "uint256", "name": "minSyOut", "type": "uint256"},
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
                "name": "mintSyFromToken",
                "outputs": [
                    {"internalType": "uint256", "name": "netSyOut", "type": "uint256"}
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "user", "type": "address"},
                    {"internalType": "address[]", "name": "sys", "type": "address[]"},
                    {"internalType": "address[]", "name": "yts", "type": "address[]"},
                    {
                        "internalType": "address[]",
                        "name": "markets",
                        "type": "address[]",
                    },
                ],
                "name": "redeemDueInterestAndRewards",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "YT", "type": "address"},
                    {"internalType": "uint256", "name": "netPyIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minSyOut", "type": "uint256"},
                ],
                "name": "redeemPyToSy",
                "outputs": [
                    {"internalType": "uint256", "name": "netSyOut", "type": "uint256"}
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "YT", "type": "address"},
                    {"internalType": "uint256", "name": "netPyIn", "type": "uint256"},
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
                "name": "redeemPyToToken",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "netTokenOut",
                        "type": "uint256",
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "SY", "type": "address"},
                    {"internalType": "uint256", "name": "netSyIn", "type": "uint256"},
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
                "name": "redeemSyToToken",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "netTokenOut",
                        "type": "uint256",
                    }
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
            {
                "inputs": [
                    {"internalType": "int256", "name": "ptToAccount", "type": "int256"},
                    {"internalType": "int256", "name": "syToAccount", "type": "int256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "swapCallback",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "exactPtIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minSyOut", "type": "uint256"},
                ],
                "name": "swapExactPtForSy",
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
                    {"internalType": "uint256", "name": "exactPtIn", "type": "uint256"},
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
                "name": "swapExactPtForToken",
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
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "exactPtIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minYtOut", "type": "uint256"},
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
                        "name": "guessTotalPtToSwap",
                        "type": "tuple",
                    },
                ],
                "name": "swapExactPtForYt",
                "outputs": [
                    {"internalType": "uint256", "name": "netYtOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "exactSyIn", "type": "uint256"},
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
                "name": "swapExactSyForPt",
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
                    {"internalType": "uint256", "name": "exactSyIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minYtOut", "type": "uint256"},
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
                        "name": "guessYtOut",
                        "type": "tuple",
                    },
                ],
                "name": "swapExactSyForYt",
                "outputs": [
                    {"internalType": "uint256", "name": "netYtOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
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
                "name": "swapExactTokenForPt",
                "outputs": [
                    {"internalType": "uint256", "name": "netPtOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "minYtOut", "type": "uint256"},
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
                        "name": "guessYtOut",
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
                "name": "swapExactTokenForYt",
                "outputs": [
                    {"internalType": "uint256", "name": "netYtOut", "type": "uint256"},
                    {"internalType": "uint256", "name": "netSyFee", "type": "uint256"},
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {"internalType": "uint256", "name": "exactYtIn", "type": "uint256"},
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
                        "name": "guessTotalPtSwapped",
                        "type": "tuple",
                    },
                ],
                "name": "swapExactYtForPt",
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
                    {"internalType": "uint256", "name": "exactYtIn", "type": "uint256"},
                    {"internalType": "uint256", "name": "minSyOut", "type": "uint256"},
                ],
                "name": "swapExactYtForSy",
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
                    {"internalType": "uint256", "name": "netYtIn", "type": "uint256"},
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
                "name": "swapExactYtForToken",
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
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "market", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "exactSyOut",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "maxPtIn", "type": "uint256"},
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
                        "name": "guessPtIn",
                        "type": "tuple",
                    },
                ],
                "name": "swapPtForExactSy",
                "outputs": [
                    {"internalType": "uint256", "name": "netPtIn", "type": "uint256"},
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
                        "name": "exactPtOut",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "maxSyIn", "type": "uint256"},
                ],
                "name": "swapSyForExactPt",
                "outputs": [
                    {"internalType": "uint256", "name": "netSyIn", "type": "uint256"},
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
                        "name": "exactYtOut",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "maxSyIn", "type": "uint256"},
                ],
                "name": "swapSyForExactYt",
                "outputs": [
                    {"internalType": "uint256", "name": "netSyIn", "type": "uint256"},
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
                        "name": "exactSyOut",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "maxYtIn", "type": "uint256"},
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
                        "name": "guessYtIn",
                        "type": "tuple",
                    },
                ],
                "name": "swapYtForExactSy",
                "outputs": [
                    {"internalType": "uint256", "name": "netYtIn", "type": "uint256"},
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

    def approve_inf(
        self, a0: List[MultiApproval], override_tx_parameters: Optional[TxParams] = None
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.approveInf(serialize_struct(a0)).build_transaction(
            override_tx_parameters
        )

    def batch_exec(
        self, calls: List[Call3], override_tx_parameters: Optional[TxParams] = None
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.batchExec(serialize_struct(calls)).build_transaction(
            override_tx_parameters
        )

    def facet_address(self, _function_selector: bytes) -> str:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.facetAddress(_function_selector).call()

    def facet_addresses(self) -> List[str]:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.facetAddresses().call()

    def facet_function_selectors(self, _facet: str) -> List[bytes]:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.facetFunctionSelectors(_facet).call()

    def facets(self) -> List[tuple]:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.facets().call()

    def mint_py_from_sy(
        self,
        receiver: str,
        y_t: str,
        net_sy_in: int,
        min_py_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.mintPyFromSy(
            receiver, y_t, net_sy_in, min_py_out
        ).build_transaction(override_tx_parameters)

    def mint_py_from_token(
        self,
        receiver: str,
        y_t: str,
        min_py_out: int,
        input: TokenInput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.mintPyFromToken(
            receiver, y_t, min_py_out, serialize_struct(input)
        ).build_transaction(override_tx_parameters)

    def mint_sy_from_token(
        self,
        receiver: str,
        s_y: str,
        min_sy_out: int,
        input: TokenInput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.mintSyFromToken(
            receiver, s_y, min_sy_out, serialize_struct(input)
        ).build_transaction(override_tx_parameters)

    def redeem_due_interest_and_rewards(
        self,
        user: str,
        sys: List[str],
        yts: List[str],
        markets: List[str],
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.redeemDueInterestAndRewards(
            user, sys, yts, markets
        ).build_transaction(override_tx_parameters)

    def redeem_py_to_sy(
        self,
        receiver: str,
        y_t: str,
        net_py_in: int,
        min_sy_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.redeemPyToSy(
            receiver, y_t, net_py_in, min_sy_out
        ).build_transaction(override_tx_parameters)

    def redeem_py_to_token(
        self,
        receiver: str,
        y_t: str,
        net_py_in: int,
        output: TokenOutput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.redeemPyToToken(
            receiver, y_t, net_py_in, serialize_struct(output)
        ).build_transaction(override_tx_parameters)

    def redeem_sy_to_token(
        self,
        receiver: str,
        s_y: str,
        net_sy_in: int,
        output: TokenOutput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.redeemSyToToken(
            receiver, s_y, net_sy_in, serialize_struct(output)
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

    def swap_callback(
        self,
        pt_to_account: int,
        sy_to_account: int,
        data: bytes,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapCallback(
            pt_to_account, sy_to_account, data
        ).build_transaction(override_tx_parameters)

    def swap_exact_pt_for_sy(
        self,
        receiver: str,
        market: str,
        exact_pt_in: int,
        min_sy_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactPtForSy(
            receiver, market, exact_pt_in, min_sy_out
        ).build_transaction(override_tx_parameters)

    def swap_exact_pt_for_token(
        self,
        receiver: str,
        market: str,
        exact_pt_in: int,
        output: TokenOutput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactPtForToken(
            receiver, market, exact_pt_in, serialize_struct(output)
        ).build_transaction(override_tx_parameters)

    def swap_exact_pt_for_yt(
        self,
        receiver: str,
        market: str,
        exact_pt_in: int,
        min_yt_out: int,
        guess_total_pt_to_swap: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactPtForYt(
            receiver,
            market,
            exact_pt_in,
            min_yt_out,
            serialize_struct(guess_total_pt_to_swap),
        ).build_transaction(override_tx_parameters)

    def swap_exact_sy_for_pt(
        self,
        receiver: str,
        market: str,
        exact_sy_in: int,
        min_pt_out: int,
        guess_pt_out: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactSyForPt(
            receiver, market, exact_sy_in, min_pt_out, serialize_struct(guess_pt_out)
        ).build_transaction(override_tx_parameters)

    def swap_exact_sy_for_yt(
        self,
        receiver: str,
        market: str,
        exact_sy_in: int,
        min_yt_out: int,
        guess_yt_out: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactSyForYt(
            receiver, market, exact_sy_in, min_yt_out, serialize_struct(guess_yt_out)
        ).build_transaction(override_tx_parameters)

    def swap_exact_token_for_pt(
        self,
        receiver: str,
        market: str,
        min_pt_out: int,
        guess_pt_out: ApproxParams,
        input: TokenInput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactTokenForPt(
            receiver,
            market,
            min_pt_out,
            serialize_struct(guess_pt_out),
            serialize_struct(input),
        ).build_transaction(override_tx_parameters)

    def swap_exact_token_for_yt(
        self,
        receiver: str,
        market: str,
        min_yt_out: int,
        guess_yt_out: ApproxParams,
        input: TokenInput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactTokenForYt(
            receiver,
            market,
            min_yt_out,
            serialize_struct(guess_yt_out),
            serialize_struct(input),
        ).build_transaction(override_tx_parameters)

    def swap_exact_yt_for_pt(
        self,
        receiver: str,
        market: str,
        exact_yt_in: int,
        min_pt_out: int,
        guess_total_pt_swapped: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactYtForPt(
            receiver,
            market,
            exact_yt_in,
            min_pt_out,
            serialize_struct(guess_total_pt_swapped),
        ).build_transaction(override_tx_parameters)

    def swap_exact_yt_for_sy(
        self,
        receiver: str,
        market: str,
        exact_yt_in: int,
        min_sy_out: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactYtForSy(
            receiver, market, exact_yt_in, min_sy_out
        ).build_transaction(override_tx_parameters)

    def swap_exact_yt_for_token(
        self,
        receiver: str,
        market: str,
        net_yt_in: int,
        output: TokenOutput,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapExactYtForToken(
            receiver, market, net_yt_in, serialize_struct(output)
        ).build_transaction(override_tx_parameters)

    def swap_pt_for_exact_sy(
        self,
        receiver: str,
        market: str,
        exact_sy_out: int,
        max_pt_in: int,
        guess_pt_in: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapPtForExactSy(
            receiver, market, exact_sy_out, max_pt_in, serialize_struct(guess_pt_in)
        ).build_transaction(override_tx_parameters)

    def swap_sy_for_exact_pt(
        self,
        receiver: str,
        market: str,
        exact_pt_out: int,
        max_sy_in: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapSyForExactPt(
            receiver, market, exact_pt_out, max_sy_in
        ).build_transaction(override_tx_parameters)

    def swap_sy_for_exact_yt(
        self,
        receiver: str,
        market: str,
        exact_yt_out: int,
        max_sy_in: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapSyForExactYt(
            receiver, market, exact_yt_out, max_sy_in
        ).build_transaction(override_tx_parameters)

    def swap_yt_for_exact_sy(
        self,
        receiver: str,
        market: str,
        exact_sy_out: int,
        max_yt_in: int,
        guess_yt_in: ApproxParams,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapYtForExactSy(
            receiver, market, exact_sy_out, max_yt_in, serialize_struct(guess_yt_in)
        ).build_transaction(override_tx_parameters)
