from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Tuple, TypedDict

from eth_account.messages import encode_structured_data
from eth_typing import Address, ChecksumAddress
from eth_utils import keccak

from eulith_web3.common import INT_FEE_TO_FLOAT_DIVISOR
from eulith_web3.contract_bindings.i_uniswap_v3_pool import IUniswapV3Pool
from eulith_web3.erc20 import EulithERC20
from eulith_web3.exceptions import EulithRpcException
from eulith_web3.websocket import (
    SubscribeRequest,
    SubscriptionHandle,
    EulithWebsocketRequestHandler,
)

from eulith_web3.eip712_types import Eip712Data, Eip712Domain, Eip712Field


class UniswapPoolFee(int, Enum):
    FiveBips = 500
    ThirtyBips = 3000
    OneHundredBips = 10000


class EulithUniV3StartLoanRequest(TypedDict):
    borrow_token_a: EulithERC20
    borrow_amount_a: float
    borrow_token_b: Optional[EulithERC20]
    borrow_amount_b: Optional[float]
    pay_transfer_from: Optional[ChecksumAddress]
    recipient: Optional[ChecksumAddress]


class EulithUniV3StartSwapRequest(TypedDict):
    sell_token: EulithERC20
    amount: float  # positive for exact sell amount, negative for exact buy amount
    pool_address: ChecksumAddress
    fill_or_kill: bool
    sqrt_limit_price: str
    recipient: Optional[ChecksumAddress]
    pay_transfer_from: Optional[ChecksumAddress]


class EulithUniV3SwapQuoteRequest(TypedDict):
    sell_token: EulithERC20
    buy_token: EulithERC20
    amount: float
    true_for_amount_in: Optional[bool]
    fee: Optional[UniswapPoolFee]


class EulithUniswapPoolLookupRequest(TypedDict):
    token_a: EulithERC20
    token_b: EulithERC20
    fee: UniswapPoolFee


class EulithUniswapV3Pool(IUniswapV3Pool):
    def __init__(
        self,
        eulith_web3: Any,
        pool_address: ChecksumAddress,
        fee: Optional[UniswapPoolFee] = None,
        token0: Optional[ChecksumAddress] = None,
        token1: Optional[ChecksumAddress] = None,
    ) -> None:
        super().__init__(eulith_web3, pool_address)
        self.pool_fee = fee
        self.t0 = token0
        self.t1 = token1
        self.ew3 = eulith_web3

    def get_token_zero(self) -> EulithERC20:
        if not self.t0:
            self.t0 = self.ew3.to_checksum_address(self.token0())
            return EulithERC20(self.ew3, self.t0)
        else:
            return EulithERC20(self.ew3, self.t0)

    def get_token_one(self) -> EulithERC20:
        if not self.t1:
            self.t1 = self.ew3.to_checksum_address(self.token1())
            return EulithERC20(self.ew3, self.t1)
        else:
            return EulithERC20(self.ew3, self.t1)

    def get_fee(self) -> UniswapPoolFee:
        if not self.pool_fee:
            r = UniswapPoolFee(self.fee())
            self.pool_fee = r
            return r
        else:
            return self.pool_fee

    # returns price (float), fee (float as percent: i.e. 0.001 = 0.1%), swap_request (EulithUniV3StartSwapRequest)
    def get_quote(
        self,
        sell_token: EulithERC20,
        amount: float,
        true_for_amount_in: Optional[bool] = True,
        fill_or_kill: Optional[bool] = True,
        recipient: Optional[ChecksumAddress] = None,
        pay_transfer_from: Optional[ChecksumAddress] = None,
    ) -> Tuple[float, float, EulithUniV3StartSwapRequest]:

        if (
            sell_token.address != self.get_token_one().address
            and sell_token.address != self.get_token_zero().address
        ):
            raise EulithRpcException(
                "cannot start swap on pool with no matching sell token, "
                "please make sure you're requesting to swap with one of the pool's tokens"
            )

        if sell_token.address == self.get_token_zero().address:
            buy_token = self.get_token_one()
        else:
            buy_token = self.get_token_zero()

        fee = self.get_fee()

        params = EulithUniV3SwapQuoteRequest(
            sell_token=sell_token,
            buy_token=buy_token,
            amount=amount,
            fee=fee,
            true_for_amount_in=true_for_amount_in,
        )

        result = self.ew3.eulith_service.uniswap_v3_quote(params)
        price, fee, swap_request = self.ew3.parse_uni_quote_to_swap_request(
            result, fill_or_kill, recipient, pay_transfer_from
        )
        return price, fee / INT_FEE_TO_FLOAT_DIVISOR, swap_request

    def subscribe_prices(
        self, handler: EulithWebsocketRequestHandler
    ) -> SubscriptionHandle:
        subscribe_request = SubscribeRequest(
            subscription_type="uni_prices", args={"pool_address": self.address}
        )

        return self.ew3.eulith_service.subscribe(subscribe_request, handler)


@dataclass
class AceUniBurnCollect:
    chain_id: int
    liquidity: int
    tick_lower: int
    tick_upper: int
    pool: Address

    def tx_hash(self) -> bytes:
        signable_message = encode_structured_data(self.typed_data())
        return keccak(b"\x19\x01" + signable_message.header + signable_message.body)

    def typed_data(self) -> Eip712Data:
        types = {
            "EIP712Domain": [
                Eip712Field(name="name", type="string"),
                Eip712Field(name="version", type="string"),
            ],
            "AceUniBurnCollect": [
                Eip712Field(name="chainId", type="int64"),
                Eip712Field(name="liquidity", type="uint128"),
                Eip712Field(name="tickLower", type="int32"),
                Eip712Field(name="tickUpper", type="int32"),
                Eip712Field(name="pool", type="address"),
            ],
        }

        payload = Eip712Data(
            types=types,
            primaryType="AceUniBurnCollect",
            domain=Eip712Domain(name="EulithAceUniBurnCollect", version="1"),
            message={
                "chainId": self.chain_id,
                "liquidity": self.liquidity,
                "tickLower": self.tick_lower,
                "tickUpper": self.tick_upper,
                "pool": self.pool,
            },
        )

        return payload
