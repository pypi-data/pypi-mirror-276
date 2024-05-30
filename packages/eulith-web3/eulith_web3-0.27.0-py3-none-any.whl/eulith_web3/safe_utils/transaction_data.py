from eth_typing import ChecksumAddress

from eulith_web3.eip712_types import Eip712Data, Eip712Domain, Eip712Field


def get_enable_module_typed_data(
    safe_address: ChecksumAddress, chain_id: int, enable_module_tx_data: str, nonce: int
) -> Eip712Data:
    types = {
        "EIP712Domain": [
            Eip712Field(name="chainId", type="uint256"),
            Eip712Field(name="verifyingContract", type="address"),
        ],
        "SafeTx": [
            Eip712Field(name="to", type="address"),
            Eip712Field(name="value", type="uint256"),
            Eip712Field(name="data", type="bytes"),
            Eip712Field(name="operation", type="uint8"),
            Eip712Field(name="safeTxGas", type="uint256"),
            Eip712Field(name="baseGas", type="uint256"),
            Eip712Field(name="gasPrice", type="uint256"),
            Eip712Field(name="gasToken", type="address"),
            Eip712Field(name="refundReceiver", type="address"),
            Eip712Field(name="nonce", type="uint256"),
        ],
    }
    message = {
        "to": safe_address,
        "value": 0,
        "data": bytes.fromhex(enable_module_tx_data[2:]),
        "operation": 0,
        "safeTxGas": 0,
        "baseGas": 0,
        "dataGas": 0,
        "gasPrice": 0,
        "gasToken": "0x0000000000000000000000000000000000000000",
        "refundReceiver": "0x0000000000000000000000000000000000000000",
        "nonce": nonce,
    }

    payload = Eip712Data(
        types=types,
        primaryType="SafeTx",
        domain=Eip712Domain(verifyingContract=safe_address, chainId=chain_id),
        message=message,
    )

    return payload
