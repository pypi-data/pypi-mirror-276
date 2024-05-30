from typing import Optional, Union, List, Tuple, TypedDict
from eth_typing import Address, ChecksumAddress
from web3 import Web3
from web3.types import TxParams


class ContractAddressNotSet(Exception):
    pass


class ISafe:
    def __init__(
        self,
        web3: Web3,
        contract_address: Optional[Union[Address, ChecksumAddress]] = None,
    ):
        self.address: Optional[Union[Address, ChecksumAddress]] = contract_address
        self.abi = [
            {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    }
                ],
                "name": "AddedOwner",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "bytes32",
                        "name": "approvedHash",
                        "type": "bytes32",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                ],
                "name": "ApproveHash",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "handler",
                        "type": "address",
                    }
                ],
                "name": "ChangedFallbackHandler",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "guard",
                        "type": "address",
                    }
                ],
                "name": "ChangedGuard",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "threshold",
                        "type": "uint256",
                    }
                ],
                "name": "ChangedThreshold",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "module",
                        "type": "address",
                    }
                ],
                "name": "DisabledModule",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "module",
                        "type": "address",
                    }
                ],
                "name": "EnabledModule",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "bytes32",
                        "name": "txHash",
                        "type": "bytes32",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "payment",
                        "type": "uint256",
                    },
                ],
                "name": "ExecutionFailure",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "module",
                        "type": "address",
                    }
                ],
                "name": "ExecutionFromModuleFailure",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "module",
                        "type": "address",
                    }
                ],
                "name": "ExecutionFromModuleSuccess",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "bytes32",
                        "name": "txHash",
                        "type": "bytes32",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "payment",
                        "type": "uint256",
                    },
                ],
                "name": "ExecutionSuccess",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    }
                ],
                "name": "RemovedOwner",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "SafeReceived",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "initiator",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address[]",
                        "name": "owners",
                        "type": "address[]",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "threshold",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "initializer",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "fallbackHandler",
                        "type": "address",
                    },
                ],
                "name": "SafeSetup",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "bytes32",
                        "name": "msgHash",
                        "type": "bytes32",
                    }
                ],
                "name": "SignMsg",
                "type": "event",
            },
            {"stateMutability": "nonpayable", "type": "fallback"},
            {
                "inputs": [],
                "name": "VERSION",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "_threshold",
                        "type": "uint256",
                    },
                ],
                "name": "addOwnerWithThreshold",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "bytes32",
                        "name": "hashToApprove",
                        "type": "bytes32",
                    }
                ],
                "name": "approveHash",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "bytes32", "name": "", "type": "bytes32"},
                ],
                "name": "approvedHashes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "_threshold", "type": "uint256"}
                ],
                "name": "changeThreshold",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "dataHash", "type": "bytes32"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "signatures", "type": "bytes"},
                    {
                        "internalType": "uint256",
                        "name": "requiredSignatures",
                        "type": "uint256",
                    },
                ],
                "name": "checkNSignatures",
                "outputs": [],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "dataHash", "type": "bytes32"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "signatures", "type": "bytes"},
                ],
                "name": "checkSignatures",
                "outputs": [],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "prevModule",
                        "type": "address",
                    },
                    {"internalType": "address", "name": "module", "type": "address"},
                ],
                "name": "disableModule",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "domainSeparator",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "module", "type": "address"}
                ],
                "name": "enableModule",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {
                        "internalType": "enum Enum.Operation",
                        "name": "operation",
                        "type": "uint8",
                    },
                    {"internalType": "uint256", "name": "safeTxGas", "type": "uint256"},
                    {"internalType": "uint256", "name": "baseGas", "type": "uint256"},
                    {"internalType": "uint256", "name": "gasPrice", "type": "uint256"},
                    {"internalType": "address", "name": "gasToken", "type": "address"},
                    {
                        "internalType": "address",
                        "name": "refundReceiver",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "_nonce", "type": "uint256"},
                ],
                "name": "encodeTransactionData",
                "outputs": [{"internalType": "bytes", "name": "", "type": "bytes"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {
                        "internalType": "enum Enum.Operation",
                        "name": "operation",
                        "type": "uint8",
                    },
                    {"internalType": "uint256", "name": "safeTxGas", "type": "uint256"},
                    {"internalType": "uint256", "name": "baseGas", "type": "uint256"},
                    {"internalType": "uint256", "name": "gasPrice", "type": "uint256"},
                    {"internalType": "address", "name": "gasToken", "type": "address"},
                    {
                        "internalType": "address payable",
                        "name": "refundReceiver",
                        "type": "address",
                    },
                    {"internalType": "bytes", "name": "signatures", "type": "bytes"},
                ],
                "name": "execTransaction",
                "outputs": [
                    {"internalType": "bool", "name": "success", "type": "bool"}
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {
                        "internalType": "enum Enum.Operation",
                        "name": "operation",
                        "type": "uint8",
                    },
                ],
                "name": "execTransactionFromModule",
                "outputs": [
                    {"internalType": "bool", "name": "success", "type": "bool"}
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {
                        "internalType": "enum Enum.Operation",
                        "name": "operation",
                        "type": "uint8",
                    },
                ],
                "name": "execTransactionFromModuleReturnData",
                "outputs": [
                    {"internalType": "bool", "name": "success", "type": "bool"},
                    {"internalType": "bytes", "name": "returnData", "type": "bytes"},
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "getChainId",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "start", "type": "address"},
                    {"internalType": "uint256", "name": "pageSize", "type": "uint256"},
                ],
                "name": "getModulesPaginated",
                "outputs": [
                    {"internalType": "address[]", "name": "array", "type": "address[]"},
                    {"internalType": "address", "name": "next", "type": "address"},
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "getOwners",
                "outputs": [
                    {"internalType": "address[]", "name": "", "type": "address[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "offset", "type": "uint256"},
                    {"internalType": "uint256", "name": "length", "type": "uint256"},
                ],
                "name": "getStorageAt",
                "outputs": [{"internalType": "bytes", "name": "", "type": "bytes"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "getThreshold",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {
                        "internalType": "enum Enum.Operation",
                        "name": "operation",
                        "type": "uint8",
                    },
                    {"internalType": "uint256", "name": "safeTxGas", "type": "uint256"},
                    {"internalType": "uint256", "name": "baseGas", "type": "uint256"},
                    {"internalType": "uint256", "name": "gasPrice", "type": "uint256"},
                    {"internalType": "address", "name": "gasToken", "type": "address"},
                    {
                        "internalType": "address",
                        "name": "refundReceiver",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "_nonce", "type": "uint256"},
                ],
                "name": "getTransactionHash",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "module", "type": "address"}
                ],
                "name": "isModuleEnabled",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "isOwner",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "nonce",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "prevOwner", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "_threshold",
                        "type": "uint256",
                    },
                ],
                "name": "removeOwner",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "handler", "type": "address"}
                ],
                "name": "setFallbackHandler",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "guard", "type": "address"}
                ],
                "name": "setGuard",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "address[]",
                        "name": "_owners",
                        "type": "address[]",
                    },
                    {
                        "internalType": "uint256",
                        "name": "_threshold",
                        "type": "uint256",
                    },
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {
                        "internalType": "address",
                        "name": "fallbackHandler",
                        "type": "address",
                    },
                    {
                        "internalType": "address",
                        "name": "paymentToken",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "payment", "type": "uint256"},
                    {
                        "internalType": "address payable",
                        "name": "paymentReceiver",
                        "type": "address",
                    },
                ],
                "name": "setup",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "name": "signedMessages",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "targetContract",
                        "type": "address",
                    },
                    {
                        "internalType": "bytes",
                        "name": "calldataPayload",
                        "type": "bytes",
                    },
                ],
                "name": "simulateAndRevert",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "prevOwner", "type": "address"},
                    {"internalType": "address", "name": "oldOwner", "type": "address"},
                    {"internalType": "address", "name": "newOwner", "type": "address"},
                ],
                "name": "swapOwner",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {"stateMutability": "payable", "type": "receive"},
        ]
        self.bytecode = "608060405234801561001057600080fd5b50600160048190555061658e80620000296000396000f3fe6080604052600436106101d15760003560e01c8063affed0e0116100f7578063e19a9dd911610095578063f08a032311610064578063f08a032314610796578063f698da25146107bf578063f8dc5dd9146107ea578063ffa1ad741461081357610226565b8063e19a9dd9146106dc578063e318b52b14610705578063e75235b81461072e578063e86637db1461075957610226565b8063cc2f8452116100d1578063cc2f84521461060f578063d4d9bdcd1461064d578063d8d11f7814610676578063e009cfde146106b357610226565b8063affed0e014610592578063b4faba09146105bd578063b63e800d146105e657610226565b80635624b25b1161016f5780636a7612021161013e5780636a761202146104d15780637d83297414610501578063934f3a111461053e578063a0e67e2b1461056757610226565b80635624b25b146104055780635ae6bd3714610442578063610b59251461047f578063694e80c3146104a857610226565b80632f54bf6e116101ab5780632f54bf6e146103225780633408e4701461035f578063468721a71461038a5780635229073f146103c757610226565b80630d582f131461029357806312fb68e0146102bc5780632d9ad53d146102e557610226565b36610226573373ffffffffffffffffffffffffffffffffffffffff167f3d0ce9bfc3ed7d6862dbb28b2dea94561fe714a1b4d019aa8af39730d1ad7c3d3460405161021c919061412e565b60405180910390a2005b34801561023257600080fd5b5060007f6c9a6c4a39284e37ed1cf53d337577d14212a4870fb976a4366c693b939918d560001b905080548061026757600080f35b36600080373360601b365260008060143601600080855af13d6000803e8061028e573d6000fd5b3d6000f35b34801561029f57600080fd5b506102ba60048036038101906102b591906141e7565b61083e565b005b3480156102c857600080fd5b506102e360048036038101906102de91906143a3565b610bc4565b005b3480156102f157600080fd5b5061030c60048036038101906103079190614442565b611203565b604051610319919061448a565b60405180910390f35b34801561032e57600080fd5b5061034960048036038101906103449190614442565b6112d5565b604051610356919061448a565b60405180910390f35b34801561036b57600080fd5b506103746113a7565b604051610381919061412e565b60405180910390f35b34801561039657600080fd5b506103b160048036038101906103ac91906144ca565b6113b4565b6040516103be919061448a565b60405180910390f35b3480156103d357600080fd5b506103ee60048036038101906103e991906144ca565b611587565b6040516103fc9291906145d5565b60405180910390f35b34801561041157600080fd5b5061042c60048036038101906104279190614605565b6115bd565b6040516104399190614645565b60405180910390f35b34801561044e57600080fd5b5061046960048036038101906104649190614667565b611655565b604051610476919061412e565b60405180910390f35b34801561048b57600080fd5b506104a660048036038101906104a19190614442565b61166d565b005b3480156104b457600080fd5b506104cf60048036038101906104ca9190614694565b61198f565b005b6104eb60048036038101906104e6919061475f565b611a63565b6040516104f8919061448a565b60405180910390f35b34801561050d57600080fd5b506105286004803603810190610523919061487b565b611e22565b604051610535919061412e565b60405180910390f35b34801561054a57600080fd5b50610565600480360381019061056091906148bb565b611e47565b005b34801561057357600080fd5b5061057c611ea3565b6040516105899190614a04565b60405180910390f35b34801561059e57600080fd5b506105a761205b565b6040516105b4919061412e565b60405180910390f35b3480156105c957600080fd5b506105e460048036038101906105df9190614a26565b612061565b005b3480156105f257600080fd5b5061060d60048036038101906106089190614ad8565b612083565b005b34801561061b57600080fd5b50610636600480360381019061063191906141e7565b6121d6565b604051610644929190614bde565b60405180910390f35b34801561065957600080fd5b50610674600480360381019061066f9190614667565b6124f2565b005b34801561068257600080fd5b5061069d60048036038101906106989190614c0e565b61265d565b6040516106aa9190614d1d565b60405180910390f35b3480156106bf57600080fd5b506106da60048036038101906106d59190614d38565b61268a565b005b3480156106e857600080fd5b5061070360048036038101906106fe9190614442565b6129ab565b005b34801561071157600080fd5b5061072c60048036038101906107279190614d78565b612b33565b005b34801561073a57600080fd5b506107436130c5565b604051610750919061412e565b60405180910390f35b34801561076557600080fd5b50610780600480360381019061077b9190614c0e565b6130cf565b60405161078d9190614645565b60405180910390f35b3480156107a257600080fd5b506107bd60048036038101906107b89190614442565b613191565b005b3480156107cb57600080fd5b506107d46131e8565b6040516107e19190614d1d565b60405180910390f35b3480156107f657600080fd5b50610811600480360381019061080c9190614dcb565b613244565b005b34801561081f57600080fd5b506108286135e2565b6040516108359190614e73565b60405180910390f35b61084661361b565b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16141580156108b05750600173ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614155b80156108e857503073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614155b610927576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161091e90614ee1565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff16600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16146109f5576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016109ec90614f4d565b60405180910390fd5b60026000600173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508160026000600173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060036000815480929190610b6590614f9c565b91905055508173ffffffffffffffffffffffffffffffffffffffff167f9465fa0c962cc76958e6373a993326400c1c94f8be2fe3a952adfa7f60b2ea2660405160405180910390a28060045414610bc057610bbf8161198f565b5b5050565b610bd860418261368b90919063ffffffff16565b82511015610c1b576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610c1290615030565b60405180910390fd5b6000808060008060005b868110156111f757610c3788826136cf565b80945081955082965050505060008460ff1603610eda5789898051906020012014610c97576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610c8e9061509c565b60405180910390fd5b8260001c9450610cb160418861368b90919063ffffffff16565b8260001c1015610cf6576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610ced90615108565b60405180910390fd5b8751610d0f60208460001c6136fe90919063ffffffff16565b1115610d50576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610d4790615174565b60405180910390fd5b60006020838a01015190508851610d8682610d7860208760001c6136fe90919063ffffffff16565b6136fe90919063ffffffff16565b1115610dc7576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610dbe906151e0565b60405180910390fd5b60606020848b010190506320c13b0b60e01b7bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19168773ffffffffffffffffffffffffffffffffffffffff166320c13b0b8d846040518363ffffffff1660e01b8152600401610e33929190615200565b602060405180830381865afa158015610e50573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610e74919061528f565b7bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191614610ed3576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610eca90615308565b60405180910390fd5b50506110a2565b60018460ff1603610fba578260001c94508473ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161480610f7657506000600860008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008c81526020019081526020016000205414155b610fb5576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610fac90615374565b60405180910390fd5b6110a1565b601e8460ff16111561104e5760018a604051602001610fd9919061540c565b60405160208183030381529060405280519060200120600486610ffc919061543f565b85856040516000815260200160405260405161101b9493929190615482565b6020604051602081039080840390855afa15801561103d573d6000803e3d6000fd5b5050506020604051035194506110a0565b60018a858585604051600081526020016040526040516110719493929190615482565b6020604051602081039080840390855afa158015611093573d6000803e3d6000fd5b5050506020604051035194505b5b5b8573ffffffffffffffffffffffffffffffffffffffff168573ffffffffffffffffffffffffffffffffffffffff161180156111695750600073ffffffffffffffffffffffffffffffffffffffff16600260008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614155b80156111a25750600173ffffffffffffffffffffffffffffffffffffffff168573ffffffffffffffffffffffffffffffffffffffff1614155b6111e1576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016111d890615513565b60405180910390fd5b84955080806111ef90614f9c565b915050610c25565b50505050505050505050565b60008173ffffffffffffffffffffffffffffffffffffffff16600173ffffffffffffffffffffffffffffffffffffffff16141580156112ce5750600073ffffffffffffffffffffffffffffffffffffffff16600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614155b9050919050565b6000600173ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16141580156113a05750600073ffffffffffffffffffffffffffffffffffffffff16600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614155b9050919050565b6000804690508091505090565b6000600173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415801561147f5750600073ffffffffffffffffffffffffffffffffffffffff16600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614155b6114be576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016114b59061557f565b60405180910390fd5b6114eb858585857fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff613726565b9050801561153b573373ffffffffffffffffffffffffffffffffffffffff167f6895c13664aa4f67288b25d7a21d7aaa34916e355fb9b6fae0a139a9085becb860405160405180910390a261157f565b3373ffffffffffffffffffffffffffffffffffffffff167facd2c8702804128fdb0db2bb49f6d127dd0181c13fd45dbfe16de0930e2bd37560405160405180910390a25b949350505050565b60006060611597868686866113b4565b915060405160203d0181016040523d81523d6000602083013e8091505094509492505050565b606060006020836115ce919061559f565b67ffffffffffffffff8111156115e7576115e6614278565b5b6040519080825280601f01601f1916602001820160405280156116195781602001600182028036833780820191505090505b50905060005b8381101561164a5780850154806020830260208501015250808061164290614f9c565b91505061161f565b508091505092915050565b60076020528060005260406000206000915090505481565b61167561361b565b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16141580156116df5750600173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614155b61171e576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161171590615645565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff16600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16146117ec576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016117e3906156b1565b60405180910390fd5b60016000600173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508060016000600173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508073ffffffffffffffffffffffffffffffffffffffff167fecdf3a3effea5783a3c4c2140e677577666428d44ed9d474a0b3a4c9943f844060405160405180910390a250565b61199761361b565b6003548111156119dc576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016119d39061571d565b60405180910390fd5b6001811015611a20576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611a1790615789565b60405180910390fd5b806004819055507f610f7ff2b304ae8903c3de74c60c6ab1f7d6226b3f52c5161905bb5ad4039c93600454604051611a58919061412e565b60405180910390a150565b6000806000611a7d8e8e8e8e8e8e8e8e8e8e6005546130cf565b905060056000815480929190611a9290614f9c565b919050555080805190602001209150611aac828286611e47565b506000611ab761377f565b9050600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614611b6f578073ffffffffffffffffffffffffffffffffffffffff166375f0bb528f8f8f8f8f8f8f8f8f8f8f336040518d63ffffffff1660e01b8152600401611b3c9c9b9a9998979695949392919061585c565b600060405180830381600087803b158015611b5657600080fd5b505af1158015611b6a573d6000803e3d6000fd5b505050505b6101f4611baa6109c48b611b839190615917565b603f60408d611b92919061559f565b611b9c919061599c565b6137b090919063ffffffff16565b611bb49190615917565b5a1015611bf6576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611bed90615a19565b60405180910390fd5b60005a9050611c688f8f8f8f8080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050508e60008d14611c54578e611c63565b6109c45a611c629190615a39565b5b613726565b9350611c7d5a826137ca90919063ffffffff16565b90508380611c8c575060008a14155b80611c98575060008814155b611cd7576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611cce90615ab9565b60405180910390fd5b600080891115611cf157611cee828b8b8b8b6137f3565b90505b8415611d3457837f442e715f626346e8c54381002da614f62bee8d27386535b2521ec8540898556e82604051611d27919061412e565b60405180910390a2611d6d565b837f23428b18acfb3ea64b08dc0c1d296ea9c09702c09083ca5272e64d115b687d2382604051611d64919061412e565b60405180910390a25b5050600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614611e11578073ffffffffffffffffffffffffffffffffffffffff16639327136883856040518363ffffffff1660e01b8152600401611dde929190615ad9565b600060405180830381600087803b158015611df857600080fd5b505af1158015611e0c573d6000803e3d6000fd5b505050505b50509b9a5050505050505050505050565b6008602052816000526040600020602052806000526040600020600091509150505481565b6000600454905060008111611e91576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611e8890615b4e565b60405180910390fd5b611e9d84848484610bc4565b50505050565b6060600060035467ffffffffffffffff811115611ec357611ec2614278565b5b604051908082528060200260200182016040528015611ef15781602001602082028036833780820191505090505b50905060008060026000600173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690505b600173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16146120525780838381518110611fa357611fa2615b6e565b5b602002602001019073ffffffffffffffffffffffffffffffffffffffff16908173ffffffffffffffffffffffffffffffffffffffff1681525050600260008273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050818061204a90614f9c565b925050611f5b565b82935050505090565b60055481565b600080825160208401855af4806000523d6020523d600060403e60403d016000fd5b6120ce8a8a80806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f8201169050808301925050505050505089613992565b600073ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff161461210c5761210b84613da0565b5b61215a8787878080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f82011690508083019250505050505050613e3d565b600082111561217457612172826000600186856137f3565b505b3373ffffffffffffffffffffffffffffffffffffffff167f141df868a6331af528e38c83b7aa03edc19be66e37ae67f9285bf4f8e3c6a1a88b8b8b8b896040516121c2959493929190615c28565b60405180910390a250505050505050505050565b60606000600173ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff16148061221a575061221984611203565b5b612259576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161225090615cc2565b60405180910390fd5b6000831161229c576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161229390615d2e565b60405180910390fd5b8267ffffffffffffffff8111156122b6576122b5614278565b5b6040519080825280602002602001820160405280156122e45781602001602082028036833780820191505090505b5091506000600160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1691505b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16141580156123b65750600173ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614155b80156123c157508381105b1561248957818382815181106123da576123d9615b6e565b5b602002602001019073ffffffffffffffffffffffffffffffffffffffff16908173ffffffffffffffffffffffffffffffffffffffff1681525050600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169150808061248190614f9c565b91505061234c565b600173ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16146124e757826001826124cb9190615a39565b815181106124dc576124db615b6e565b5b602002602001015191505b808352509250929050565b600073ffffffffffffffffffffffffffffffffffffffff16600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16036125c0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016125b790615d9a565b60405180910390fd5b6001600860003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000838152602001908152602001600020819055503373ffffffffffffffffffffffffffffffffffffffff16817ff2a0eb156472d1440255b0d7c1e19cc07115d1051fe605b0dce69acfec884d9c60405160405180910390a350565b60006126728c8c8c8c8c8c8c8c8c8c8c6130cf565b8051906020012090509b9a5050505050505050505050565b61269261361b565b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16141580156126fc5750600173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614155b61273b576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161273290615645565b60405180910390fd5b8073ffffffffffffffffffffffffffffffffffffffff16600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614612808576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016127ff90615e06565b60405180910390fd5b600160008273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506000600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508073ffffffffffffffffffffffffffffffffffffffff167faab4fa2b463f581b2b32cb3b7e3b704b9ce37cc209b5fb4d77e593ace405427660405160405180910390a25050565b6129b361361b565b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614612ac1578073ffffffffffffffffffffffffffffffffffffffff166301ffc9a77fe6d7a83a000000000000000000000000000000000000000000000000000000006040518263ffffffff1660e01b8152600401612a409190615e35565b602060405180830381865afa158015612a5d573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190612a819190615e7c565b612ac0576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612ab790615ef5565b60405180910390fd5b5b60007f4a204f620c8c5ccdca3fd54d003badd85ba500436a431f0cbda4f558c93c34c860001b90508181558173ffffffffffffffffffffffffffffffffffffffff167f1151116914515bc0891ff9047a6cb32cf902546f83066499bcf8ba33d2353fa260405160405180910390a25050565b612b3b61361b565b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614158015612ba55750600173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614155b8015612bdd57503073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614155b612c1c576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612c1390614ee1565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff16600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614612cea576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612ce190614f4d565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614158015612d545750600173ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614155b612d93576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612d8a90614ee1565b60405180910390fd5b8173ffffffffffffffffffffffffffffffffffffffff16600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614612e60576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401612e5790615f61565b60405180910390fd5b600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506000600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff167ff8d49fc529812e9a7c5c50e69c20f0dccc0db8fa95c98bc58cc9a4f1c1299eaf60405160405180910390a28073ffffffffffffffffffffffffffffffffffffffff167f9465fa0c962cc76958e6373a993326400c1c94f8be2fe3a952adfa7f60b2ea2660405160405180910390a2505050565b6000600454905090565b606060007fbb8310d486368db6bd6f849402fdd73ad53d316b5a4b2644ad6efe0f941286d860001b8d8d8d8d604051613109929190615fb1565b60405180910390208c8c8c8c8c8c8c6040516020016131329b9a99989796959493929190615fca565b604051602081830303815290604052805190602001209050601960f81b600160f81b61315c6131e8565b8360405160200161317094939291906160c2565b6040516020818303038152906040529150509b9a5050505050505050505050565b61319961361b565b6131a281613da0565b8073ffffffffffffffffffffffffffffffffffffffff167f5ac6c46c93c8d0e53714ba3b53db3e7c046da994313d7ed0d192028bc7c228b060405160405180910390a250565b60007f47e79534a245952e8b16893a336b85a3d9ea9fa8c573f3d803afb92a7946921860001b6132166113a7565b306040516020016132299392919061616f565b60405160208183030381529060405280519060200120905090565b61324c61361b565b80600160035461325c9190615a39565b101561329d576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016132949061571d565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16141580156133075750600173ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614155b613346576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161333d90614ee1565b60405180910390fd5b8173ffffffffffffffffffffffffffffffffffffffff16600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614613413576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161340a90615f61565b60405180910390fd5b600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506000600260008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060036000815480929190613582906161a6565b91905055508173ffffffffffffffffffffffffffffffffffffffff167ff8d49fc529812e9a7c5c50e69c20f0dccc0db8fa95c98bc58cc9a4f1c1299eaf60405160405180910390a280600454146135dd576135dc8161198f565b5b505050565b6040518060400160405280600581526020017f312e342e3000000000000000000000000000000000000000000000000000000081525081565b3073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614613689576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016136809061621b565b60405180910390fd5b565b600080830361369d57600090506136c9565b600082846136ab919061559f565b90508284826136ba919061599c565b146136c457600080fd5b809150505b92915050565b60008060008360410260208101860151925060408101860151915060ff60418201870151169350509250925092565b600080828461370d9190615917565b90508381101561371c57600080fd5b8091505092915050565b600060018081111561373b5761373a6157d6565b5b83600181111561374e5761374d6157d6565b5b03613766576000808551602087018986f49050613776565b600080855160208701888a87f190505b95945050505050565b6000807f4a204f620c8c5ccdca3fd54d003badd85ba500436a431f0cbda4f558c93c34c860001b9050805491505090565b6000818310156137c057816137c2565b825b905092915050565b6000828211156137d957600080fd5b600082846137e79190615a39565b90508091505092915050565b600080600073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff16146138305782613832565b325b9050600073ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff16036139165761389b3a8610613878573a61387a565b855b61388d888a6136fe90919063ffffffff16565b61368b90919063ffffffff16565b91508073ffffffffffffffffffffffffffffffffffffffff166108fc839081150290604051600060405180830381858888f19350505050613911576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161390890616287565b60405180910390fd5b613988565b61393b8561392d888a6136fe90919063ffffffff16565b61368b90919063ffffffff16565b915061394884828461405a565b613987576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161397e906162f3565b60405180910390fd5b5b5095945050505050565b6000600454146139d7576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016139ce9061635f565b60405180910390fd5b8151811115613a1b576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401613a129061571d565b60405180910390fd5b6001811015613a5f576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401613a5690615789565b60405180910390fd5b60006001905060005b8351811015613d0c576000848281518110613a8657613a85615b6e565b5b60200260200101519050600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614158015613afa5750600173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614155b8015613b3257503073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1614155b8015613b6a57508073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff1614155b613ba9576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401613ba090614ee1565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff16600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614613c77576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401613c6e90614f4d565b60405180910390fd5b80600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550809250508080613d0490614f9c565b915050613a68565b506001600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550825160038190555081600481905550505050565b3073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1603613e0e576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401613e05906163cb565b60405180910390fd5b60007f6c9a6c4a39284e37ed1cf53d337577d14212a4870fb976a4366c693b939918d560001b90508181555050565b600073ffffffffffffffffffffffffffffffffffffffff1660016000600173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614613f0c576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401613f0390616437565b60405180910390fd5b6001806000600173ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff161461405657613fc882614102565b614007576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401613ffe906164a3565b60405180910390fd5b6140168260008360015a613726565b614055576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161404c9061650f565b60405180910390fd5b5b5050565b60008063a9059cbb848460405160240161407592919061652f565b6040516020818303038152906040529060e01b6020820180517bffffffffffffffffffffffffffffffffffffffffffffffffffffffff83818316178352505050509050602060008251602084016000896127105a03f13d600081146140e557602081146140ed57600093506140f8565b8193506140f8565b600051158215171593505b5050509392505050565b600080823b905060008111915050919050565b6000819050919050565b61412881614115565b82525050565b6000602082019050614143600083018461411f565b92915050565b6000604051905090565b600080fd5b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006141888261415d565b9050919050565b6141988161417d565b81146141a357600080fd5b50565b6000813590506141b58161418f565b92915050565b6141c481614115565b81146141cf57600080fd5b50565b6000813590506141e1816141bb565b92915050565b600080604083850312156141fe576141fd614153565b5b600061420c858286016141a6565b925050602061421d858286016141d2565b9150509250929050565b6000819050919050565b61423a81614227565b811461424557600080fd5b50565b60008135905061425781614231565b92915050565b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6142b082614267565b810181811067ffffffffffffffff821117156142cf576142ce614278565b5b80604052505050565b60006142e2614149565b90506142ee82826142a7565b919050565b600067ffffffffffffffff82111561430e5761430d614278565b5b61431782614267565b9050602081019050919050565b82818337600083830152505050565b6000614346614341846142f3565b6142d8565b90508281526020810184848401111561436257614361614262565b5b61436d848285614324565b509392505050565b600082601f83011261438a5761438961425d565b5b813561439a848260208601614333565b91505092915050565b600080600080608085870312156143bd576143bc614153565b5b60006143cb87828801614248565b945050602085013567ffffffffffffffff8111156143ec576143eb614158565b5b6143f887828801614375565b935050604085013567ffffffffffffffff81111561441957614418614158565b5b61442587828801614375565b9250506060614436878288016141d2565b91505092959194509250565b60006020828403121561445857614457614153565b5b6000614466848285016141a6565b91505092915050565b60008115159050919050565b6144848161446f565b82525050565b600060208201905061449f600083018461447b565b92915050565b600281106144b257600080fd5b50565b6000813590506144c4816144a5565b92915050565b600080600080608085870312156144e4576144e3614153565b5b60006144f2878288016141a6565b9450506020614503878288016141d2565b935050604085013567ffffffffffffffff81111561452457614523614158565b5b61453087828801614375565b9250506060614541878288016144b5565b91505092959194509250565b600081519050919050565b600082825260208201905092915050565b60005b8381101561458757808201518184015260208101905061456c565b83811115614596576000848401525b50505050565b60006145a78261454d565b6145b18185614558565b93506145c1818560208601614569565b6145ca81614267565b840191505092915050565b60006040820190506145ea600083018561447b565b81810360208301526145fc818461459c565b90509392505050565b6000806040838503121561461c5761461b614153565b5b600061462a858286016141d2565b925050602061463b858286016141d2565b9150509250929050565b6000602082019050818103600083015261465f818461459c565b905092915050565b60006020828403121561467d5761467c614153565b5b600061468b84828501614248565b91505092915050565b6000602082840312156146aa576146a9614153565b5b60006146b8848285016141d2565b91505092915050565b600080fd5b600080fd5b60008083601f8401126146e1576146e061425d565b5b8235905067ffffffffffffffff8111156146fe576146fd6146c1565b5b60208301915083600182028301111561471a576147196146c6565b5b9250929050565b600061472c8261415d565b9050919050565b61473c81614721565b811461474757600080fd5b50565b60008135905061475981614733565b92915050565b60008060008060008060008060008060006101408c8e03121561478557614784614153565b5b60006147938e828f016141a6565b9b505060206147a48e828f016141d2565b9a505060408c013567ffffffffffffffff8111156147c5576147c4614158565b5b6147d18e828f016146cb565b995099505060606147e48e828f016144b5565b97505060806147f58e828f016141d2565b96505060a06148068e828f016141d2565b95505060c06148178e828f016141d2565b94505060e06148288e828f016141a6565b93505061010061483a8e828f0161474a565b9250506101208c013567ffffffffffffffff81111561485c5761485b614158565b5b6148688e828f01614375565b9150509295989b509295989b9093969950565b6000806040838503121561489257614891614153565b5b60006148a0858286016141a6565b92505060206148b185828601614248565b9150509250929050565b6000806000606084860312156148d4576148d3614153565b5b60006148e286828701614248565b935050602084013567ffffffffffffffff81111561490357614902614158565b5b61490f86828701614375565b925050604084013567ffffffffffffffff8111156149305761492f614158565b5b61493c86828701614375565b9150509250925092565b600081519050919050565b600082825260208201905092915050565b6000819050602082019050919050565b61497b8161417d565b82525050565b600061498d8383614972565b60208301905092915050565b6000602082019050919050565b60006149b182614946565b6149bb8185614951565b93506149c683614962565b8060005b838110156149f75781516149de8882614981565b97506149e983614999565b9250506001810190506149ca565b5085935050505092915050565b60006020820190508181036000830152614a1e81846149a6565b905092915050565b60008060408385031215614a3d57614a3c614153565b5b6000614a4b858286016141a6565b925050602083013567ffffffffffffffff811115614a6c57614a6b614158565b5b614a7885828601614375565b9150509250929050565b60008083601f840112614a9857614a9761425d565b5b8235905067ffffffffffffffff811115614ab557614ab46146c1565b5b602083019150836020820283011115614ad157614ad06146c6565b5b9250929050565b6000806000806000806000806000806101008b8d031215614afc57614afb614153565b5b60008b013567ffffffffffffffff811115614b1a57614b19614158565b5b614b268d828e01614a82565b9a509a50506020614b398d828e016141d2565b9850506040614b4a8d828e016141a6565b97505060608b013567ffffffffffffffff811115614b6b57614b6a614158565b5b614b778d828e016146cb565b96509650506080614b8a8d828e016141a6565b94505060a0614b9b8d828e016141a6565b93505060c0614bac8d828e016141d2565b92505060e0614bbd8d828e0161474a565b9150509295989b9194979a5092959850565b614bd88161417d565b82525050565b60006040820190508181036000830152614bf881856149a6565b9050614c076020830184614bcf565b9392505050565b60008060008060008060008060008060006101408c8e031215614c3457614c33614153565b5b6000614c428e828f016141a6565b9b50506020614c538e828f016141d2565b9a505060408c013567ffffffffffffffff811115614c7457614c73614158565b5b614c808e828f016146cb565b99509950506060614c938e828f016144b5565b9750506080614ca48e828f016141d2565b96505060a0614cb58e828f016141d2565b95505060c0614cc68e828f016141d2565b94505060e0614cd78e828f016141a6565b935050610100614ce98e828f016141a6565b925050610120614cfb8e828f016141d2565b9150509295989b509295989b9093969950565b614d1781614227565b82525050565b6000602082019050614d326000830184614d0e565b92915050565b60008060408385031215614d4f57614d4e614153565b5b6000614d5d858286016141a6565b9250506020614d6e858286016141a6565b9150509250929050565b600080600060608486031215614d9157614d90614153565b5b6000614d9f868287016141a6565b9350506020614db0868287016141a6565b9250506040614dc1868287016141a6565b9150509250925092565b600080600060608486031215614de457614de3614153565b5b6000614df2868287016141a6565b9350506020614e03868287016141a6565b9250506040614e14868287016141d2565b9150509250925092565b600081519050919050565b600082825260208201905092915050565b6000614e4582614e1e565b614e4f8185614e29565b9350614e5f818560208601614569565b614e6881614267565b840191505092915050565b60006020820190508181036000830152614e8d8184614e3a565b905092915050565b7f4753323033000000000000000000000000000000000000000000000000000000600082015250565b6000614ecb600583614e29565b9150614ed682614e95565b602082019050919050565b60006020820190508181036000830152614efa81614ebe565b9050919050565b7f4753323034000000000000000000000000000000000000000000000000000000600082015250565b6000614f37600583614e29565b9150614f4282614f01565b602082019050919050565b60006020820190508181036000830152614f6681614f2a565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000614fa782614115565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8203614fd957614fd8614f6d565b5b600182019050919050565b7f4753303230000000000000000000000000000000000000000000000000000000600082015250565b600061501a600583614e29565b915061502582614fe4565b602082019050919050565b600060208201905081810360008301526150498161500d565b9050919050565b7f4753303237000000000000000000000000000000000000000000000000000000600082015250565b6000615086600583614e29565b915061509182615050565b602082019050919050565b600060208201905081810360008301526150b581615079565b9050919050565b7f4753303231000000000000000000000000000000000000000000000000000000600082015250565b60006150f2600583614e29565b91506150fd826150bc565b602082019050919050565b60006020820190508181036000830152615121816150e5565b9050919050565b7f4753303232000000000000000000000000000000000000000000000000000000600082015250565b600061515e600583614e29565b915061516982615128565b602082019050919050565b6000602082019050818103600083015261518d81615151565b9050919050565b7f4753303233000000000000000000000000000000000000000000000000000000600082015250565b60006151ca600583614e29565b91506151d582615194565b602082019050919050565b600060208201905081810360008301526151f9816151bd565b9050919050565b6000604082019050818103600083015261521a818561459c565b9050818103602083015261522e818461459c565b90509392505050565b60007fffffffff0000000000000000000000000000000000000000000000000000000082169050919050565b61526c81615237565b811461527757600080fd5b50565b60008151905061528981615263565b92915050565b6000602082840312156152a5576152a4614153565b5b60006152b38482850161527a565b91505092915050565b7f4753303234000000000000000000000000000000000000000000000000000000600082015250565b60006152f2600583614e29565b91506152fd826152bc565b602082019050919050565b60006020820190508181036000830152615321816152e5565b9050919050565b7f4753303235000000000000000000000000000000000000000000000000000000600082015250565b600061535e600583614e29565b915061536982615328565b602082019050919050565b6000602082019050818103600083015261538d81615351565b9050919050565b600081905092915050565b7f19457468657265756d205369676e6564204d6573736167653a0a333200000000600082015250565b60006153d5601c83615394565b91506153e08261539f565b601c82019050919050565b6000819050919050565b61540661540182614227565b6153eb565b82525050565b6000615417826153c8565b915061542382846153f5565b60208201915081905092915050565b600060ff82169050919050565b600061544a82615432565b915061545583615432565b92508282101561546857615467614f6d565b5b828203905092915050565b61547c81615432565b82525050565b60006080820190506154976000830187614d0e565b6154a46020830186615473565b6154b16040830185614d0e565b6154be6060830184614d0e565b95945050505050565b7f4753303236000000000000000000000000000000000000000000000000000000600082015250565b60006154fd600583614e29565b9150615508826154c7565b602082019050919050565b6000602082019050818103600083015261552c816154f0565b9050919050565b7f4753313034000000000000000000000000000000000000000000000000000000600082015250565b6000615569600583614e29565b915061557482615533565b602082019050919050565b600060208201905081810360008301526155988161555c565b9050919050565b60006155aa82614115565b91506155b583614115565b9250817fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff04831182151516156155ee576155ed614f6d565b5b828202905092915050565b7f4753313031000000000000000000000000000000000000000000000000000000600082015250565b600061562f600583614e29565b915061563a826155f9565b602082019050919050565b6000602082019050818103600083015261565e81615622565b9050919050565b7f4753313032000000000000000000000000000000000000000000000000000000600082015250565b600061569b600583614e29565b91506156a682615665565b602082019050919050565b600060208201905081810360008301526156ca8161568e565b9050919050565b7f4753323031000000000000000000000000000000000000000000000000000000600082015250565b6000615707600583614e29565b9150615712826156d1565b602082019050919050565b60006020820190508181036000830152615736816156fa565b9050919050565b7f4753323032000000000000000000000000000000000000000000000000000000600082015250565b6000615773600583614e29565b915061577e8261573d565b602082019050919050565b600060208201905081810360008301526157a281615766565b9050919050565b60006157b58385614558565b93506157c2838584614324565b6157cb83614267565b840190509392505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602160045260246000fd5b60028110615816576158156157d6565b5b50565b600081905061582782615805565b919050565b600061583782615819565b9050919050565b6158478161582c565b82525050565b61585681614721565b82525050565b600061016082019050615872600083018f614bcf565b61587f602083018e61411f565b8181036040830152615892818c8e6157a9565b90506158a1606083018b61583e565b6158ae608083018a61411f565b6158bb60a083018961411f565b6158c860c083018861411f565b6158d560e0830187614bcf565b6158e361010083018661584d565b8181036101208301526158f6818561459c565b9050615906610140830184614bcf565b9d9c50505050505050505050505050565b600061592282614115565b915061592d83614115565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0382111561596257615961614f6d565b5b828201905092915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601260045260246000fd5b60006159a782614115565b91506159b283614115565b9250826159c2576159c161596d565b5b828204905092915050565b7f4753303130000000000000000000000000000000000000000000000000000000600082015250565b6000615a03600583614e29565b9150615a0e826159cd565b602082019050919050565b60006020820190508181036000830152615a32816159f6565b9050919050565b6000615a4482614115565b9150615a4f83614115565b925082821015615a6257615a61614f6d565b5b828203905092915050565b7f4753303133000000000000000000000000000000000000000000000000000000600082015250565b6000615aa3600583614e29565b9150615aae82615a6d565b602082019050919050565b60006020820190508181036000830152615ad281615a96565b9050919050565b6000604082019050615aee6000830185614d0e565b615afb602083018461447b565b9392505050565b7f4753303031000000000000000000000000000000000000000000000000000000600082015250565b6000615b38600583614e29565b9150615b4382615b02565b602082019050919050565b60006020820190508181036000830152615b6781615b2b565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b6000819050919050565b6000615bb660208401846141a6565b905092915050565b6000602082019050919050565b6000615bd78385614951565b9350615be282615b9d565b8060005b85811015615c1b57615bf88284615ba7565b615c028882614981565b9750615c0d83615bbe565b925050600181019050615be6565b5085925050509392505050565b60006080820190508181036000830152615c43818789615bcb565b9050615c52602083018661411f565b615c5f6040830185614bcf565b615c6c6060830184614bcf565b9695505050505050565b7f4753313035000000000000000000000000000000000000000000000000000000600082015250565b6000615cac600583614e29565b9150615cb782615c76565b602082019050919050565b60006020820190508181036000830152615cdb81615c9f565b9050919050565b7f4753313036000000000000000000000000000000000000000000000000000000600082015250565b6000615d18600583614e29565b9150615d2382615ce2565b602082019050919050565b60006020820190508181036000830152615d4781615d0b565b9050919050565b7f4753303330000000000000000000000000000000000000000000000000000000600082015250565b6000615d84600583614e29565b9150615d8f82615d4e565b602082019050919050565b60006020820190508181036000830152615db381615d77565b9050919050565b7f4753313033000000000000000000000000000000000000000000000000000000600082015250565b6000615df0600583614e29565b9150615dfb82615dba565b602082019050919050565b60006020820190508181036000830152615e1f81615de3565b9050919050565b615e2f81615237565b82525050565b6000602082019050615e4a6000830184615e26565b92915050565b615e598161446f565b8114615e6457600080fd5b50565b600081519050615e7681615e50565b92915050565b600060208284031215615e9257615e91614153565b5b6000615ea084828501615e67565b91505092915050565b7f4753333030000000000000000000000000000000000000000000000000000000600082015250565b6000615edf600583614e29565b9150615eea82615ea9565b602082019050919050565b60006020820190508181036000830152615f0e81615ed2565b9050919050565b7f4753323035000000000000000000000000000000000000000000000000000000600082015250565b6000615f4b600583614e29565b9150615f5682615f15565b602082019050919050565b60006020820190508181036000830152615f7a81615f3e565b9050919050565b600081905092915050565b6000615f988385615f81565b9350615fa5838584614324565b82840190509392505050565b6000615fbe828486615f8c565b91508190509392505050565b600061016082019050615fe0600083018e614d0e565b615fed602083018d614bcf565b615ffa604083018c61411f565b616007606083018b614d0e565b616014608083018a61583e565b61602160a083018961411f565b61602e60c083018861411f565b61603b60e083018761411f565b616049610100830186614bcf565b616057610120830185614bcf565b61606561014083018461411f565b9c9b505050505050505050505050565b60007fff0000000000000000000000000000000000000000000000000000000000000082169050919050565b6000819050919050565b6160bc6160b782616075565b6160a1565b82525050565b60006160ce82876160ab565b6001820191506160de82866160ab565b6001820191506160ee82856153f5565b6020820191506160fe82846153f5565b60208201915081905095945050505050565b6000819050919050565b600061613561613061612b8461415d565b616110565b61415d565b9050919050565b60006161478261611a565b9050919050565b60006161598261613c565b9050919050565b6161698161614e565b82525050565b60006060820190506161846000830186614d0e565b616191602083018561411f565b61619e6040830184616160565b949350505050565b60006161b182614115565b9150600082036161c4576161c3614f6d565b5b600182039050919050565b7f4753303331000000000000000000000000000000000000000000000000000000600082015250565b6000616205600583614e29565b9150616210826161cf565b602082019050919050565b60006020820190508181036000830152616234816161f8565b9050919050565b7f4753303131000000000000000000000000000000000000000000000000000000600082015250565b6000616271600583614e29565b915061627c8261623b565b602082019050919050565b600060208201905081810360008301526162a081616264565b9050919050565b7f4753303132000000000000000000000000000000000000000000000000000000600082015250565b60006162dd600583614e29565b91506162e8826162a7565b602082019050919050565b6000602082019050818103600083015261630c816162d0565b9050919050565b7f4753323030000000000000000000000000000000000000000000000000000000600082015250565b6000616349600583614e29565b915061635482616313565b602082019050919050565b600060208201905081810360008301526163788161633c565b9050919050565b7f4753343030000000000000000000000000000000000000000000000000000000600082015250565b60006163b5600583614e29565b91506163c08261637f565b602082019050919050565b600060208201905081810360008301526163e4816163a8565b9050919050565b7f4753313030000000000000000000000000000000000000000000000000000000600082015250565b6000616421600583614e29565b915061642c826163eb565b602082019050919050565b6000602082019050818103600083015261645081616414565b9050919050565b7f4753303032000000000000000000000000000000000000000000000000000000600082015250565b600061648d600583614e29565b915061649882616457565b602082019050919050565b600060208201905081810360008301526164bc81616480565b9050919050565b7f4753303030000000000000000000000000000000000000000000000000000000600082015250565b60006164f9600583614e29565b9150616504826164c3565b602082019050919050565b60006020820190508181036000830152616528816164ec565b9050919050565b60006040820190506165446000830185614bcf565b616551602083018461411f565b939250505056fea264697066735822122088cc34401db63adcbf1dce6daa7b5cda405d9959d6f52974867d742980d99bfe64736f6c634300080f0033"
        self.w3 = web3

    def deploy(self):
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = contract.constructor().transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        self.address = tx_receipt.contractAddress

    def v_e_r_s_i_o_n(self) -> str:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.VERSION().call()

    def add_owner_with_threshold(
        self,
        owner: str,
        _threshold: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.addOwnerWithThreshold(owner, _threshold).build_transaction(
            override_tx_parameters
        )

    def approve_hash(
        self, hash_to_approve: bytes, override_tx_parameters: Optional[TxParams] = None
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.approveHash(hash_to_approve).build_transaction(
            override_tx_parameters
        )

    def approved_hashes(self, a0: str, a1: bytes) -> int:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.approvedHashes(a0, a1).call()

    def change_threshold(
        self, _threshold: int, override_tx_parameters: Optional[TxParams] = None
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.changeThreshold(_threshold).build_transaction(
            override_tx_parameters
        )

    def check_n_signatures(
        self, data_hash: bytes, data: bytes, signatures: bytes, required_signatures: int
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.checkNSignatures(
            data_hash, data, signatures, required_signatures
        ).build_transaction()

    def check_signatures(
        self, data_hash: bytes, data: bytes, signatures: bytes
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.checkSignatures(
            data_hash, data, signatures
        ).build_transaction()

    def disable_module(
        self,
        prev_module: str,
        module: str,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.disableModule(prev_module, module).build_transaction(
            override_tx_parameters
        )

    def domain_separator(self) -> bytes:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.domainSeparator().call()

    def enable_module(
        self, module: str, override_tx_parameters: Optional[TxParams] = None
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.enableModule(module).build_transaction(
            override_tx_parameters
        )

    def encode_transaction_data(
        self,
        to: str,
        value: int,
        data: bytes,
        operation: int,
        safe_tx_gas: int,
        base_gas: int,
        gas_price: int,
        gas_token: str,
        refund_receiver: str,
        _nonce: int,
    ) -> bytes:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.encodeTransactionData(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            _nonce,
        ).call()

    def exec_transaction(
        self,
        to: str,
        value: int,
        data: bytes,
        operation: int,
        safe_tx_gas: int,
        base_gas: int,
        gas_price: int,
        gas_token: str,
        refund_receiver: None,
        signatures: bytes,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.execTransaction(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            signatures,
        ).build_transaction(override_tx_parameters)

    def exec_transaction_from_module(
        self,
        to: str,
        value: int,
        data: bytes,
        operation: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.execTransactionFromModule(
            to, value, data, operation
        ).build_transaction(override_tx_parameters)

    def exec_transaction_from_module_return_data(
        self,
        to: str,
        value: int,
        data: bytes,
        operation: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.execTransactionFromModuleReturnData(
            to, value, data, operation
        ).build_transaction(override_tx_parameters)

    def get_chain_id(self) -> int:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.getChainId().call()

    def get_modules_paginated(
        self, start: str, page_size: int
    ) -> Tuple[List[str], str]:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.getModulesPaginated(start, page_size).call()

    def get_owners(self) -> List[str]:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.getOwners().call()

    def get_storage_at(self, offset: int, length: int) -> bytes:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.getStorageAt(offset, length).call()

    def get_threshold(self) -> int:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.getThreshold().call()

    def get_transaction_hash(
        self,
        to: str,
        value: int,
        data: bytes,
        operation: int,
        safe_tx_gas: int,
        base_gas: int,
        gas_price: int,
        gas_token: str,
        refund_receiver: str,
        _nonce: int,
    ) -> bytes:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.getTransactionHash(
            to,
            value,
            data,
            operation,
            safe_tx_gas,
            base_gas,
            gas_price,
            gas_token,
            refund_receiver,
            _nonce,
        ).call()

    def is_module_enabled(self, module: str) -> bool:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.isModuleEnabled(module).call()

    def is_owner(self, owner: str) -> bool:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.isOwner(owner).call()

    def nonce(self) -> int:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.nonce().call()

    def remove_owner(
        self,
        prev_owner: str,
        owner: str,
        _threshold: int,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.removeOwner(prev_owner, owner, _threshold).build_transaction(
            override_tx_parameters
        )

    def set_fallback_handler(
        self, handler: str, override_tx_parameters: Optional[TxParams] = None
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.setFallbackHandler(handler).build_transaction(
            override_tx_parameters
        )

    def set_guard(
        self, guard: str, override_tx_parameters: Optional[TxParams] = None
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.setGuard(guard).build_transaction(override_tx_parameters)

    def setup(
        self,
        _owners: List[str],
        _threshold: int,
        to: str,
        data: bytes,
        fallback_handler: str,
        payment_token: str,
        payment: int,
        payment_receiver: None,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.setup(
            _owners,
            _threshold,
            to,
            data,
            fallback_handler,
            payment_token,
            payment,
            payment_receiver,
        ).build_transaction(override_tx_parameters)

    def signed_messages(self, a0: bytes) -> int:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.signedMessages(a0).call()

    def simulate_and_revert(
        self,
        target_contract: str,
        calldata_payload: bytes,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.simulateAndRevert(
            target_contract, calldata_payload
        ).build_transaction(override_tx_parameters)

    def swap_owner(
        self,
        prev_owner: str,
        old_owner: str,
        new_owner: str,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        if not self.address:
            raise ContractAddressNotSet(
                "you must either deploy or initialize the contract with an address"
            )
        c = self.w3.eth.contract(address=self.address, abi=self.abi)

        return c.functions.swapOwner(
            prev_owner, old_owner, new_owner
        ).build_transaction(override_tx_parameters)
