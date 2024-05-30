from enum import Enum
from typing import Any, Dict, Optional, Union, cast

from eth_typing import ChecksumAddress
from web3.types import TxParams

from eulith_web3.erc20 import EulithERC20
from eulith_web3.exceptions import EulithRpcException


class PendleClientException(Exception):
    pass


class PendlePtQuote:
    """
    Represents a quote for buying Pendle Token (PT) in exchange for underlying assets.

    :ivar price_denom_underlying: The PT price in terms of the underlying asset.
    :vartype price_denom_underlying: Optional[float]

    :ivar implied_yield: The current implied yield (as of the last trade).
    :vartype implied_yield: Optional[float]

    :ivar sy_underlying_exchange_rate: The exchange rate of the underlying asset to the SY asset.
    :vartype sy_underlying_exchange_rate: Optional[float]
    """

    def __init__(self, from_dict: Dict[Any, Any]) -> None:
        self.price_denom_underlying: Optional[float] = None
        self.implied_yield: Optional[float] = None
        self.sy_underlying_exchange_rate: Optional[float] = None

        for key, val in from_dict.items():
            setattr(self, key, val)


class PendleSwap:
    """
    The PendleSwap class encapsulates response data from the Eulith server in convenient typed fields

    :ivar sell_token: The token to be sold.
    :vartype sell_token: Optional[EulithERC20]
    :ivar buy_token: The token to be bought.
    :vartype buy_token: Optional[EulithERC20]
    :ivar sell_amount: The amount of sell token to be sold.
    :vartype sell_amount: Optional[float]
    :ivar buy_amount: The amount of buy token to be bought.
    :vartype buy_amount: Optional[float]
    :ivar approve_address: The ERC20 address you need to approve(sell_amount) for the swap to work
    :vartype approve_address: Optional[ChecksumAddress]
    :ivar tx: The transaction parameters.
    :vartype tx: Optional[TxParams]
    """

    def __init__(self, ew3: Any, from_dict: Dict[Any, Any]):
        """
        :param ew3: The Eulith web3 instance.
        :param from_dict: Response body from the Eulith Pendle Swap request
        """
        self.sell_token: Optional[EulithERC20] = None
        self.buy_token: Optional[EulithERC20] = None
        self.sell_amount: Optional[float] = None
        self.buy_amount: Optional[float] = None
        self.approve_address: Optional[ChecksumAddress] = None
        self.tx: Optional[TxParams] = None

        for key, val in from_dict.items():
            if key == "sell_token" or key == "buy_token":
                setattr(self, key, EulithERC20(ew3, ew3.to_checksum_address(val)))
            elif key == "approve_address":
                setattr(self, key, ew3.to_checksum_address(val))
            else:
                setattr(self, key, val)


class PendleMarketSymbol(str, Enum):
    PT = "pt"
    YT = "yt"


class PendleClient:
    def __init__(
        self, ew3: Any, router_override: Optional[ChecksumAddress] = None
    ) -> None:
        self.ew3 = ew3

        # Default address from https://docs.pendle.finance/Developers/DeployedContracts/Ethereum
        # Default address is true for both Ethereum and Arbitrum
        self.router = (
            router_override
            if router_override
            else self.ew3.to_checksum_address(
                "0x0000000001e4ef00d069e71d6ba041b0a16f7ea0"
            )
        )

    def quote_pt(
        self, buy_pt_amount: float, market_address: ChecksumAddress
    ) -> PendlePtQuote:
        """
        Get a quote for buying a certain amount of Pendle Token (PT) in exchange for underlying assets.

        :param buy_pt_amount: The amount of PT to buy.
        :param market_address: The address of the Pendle market to buy PT from.

        :return: A PendlePtQuote object containing the PT purchase quote.
        """
        result = self.ew3.eulith_service.get_pt_quote(buy_pt_amount, market_address)
        return PendlePtQuote(result)

    def swap(
        self,
        sell_token: Union[EulithERC20, PendleMarketSymbol],
        buy_token: Union[EulithERC20, PendleMarketSymbol],
        sell_amount: float,
        slippage: float,
        pendle_market: ChecksumAddress,
        recipient: Optional[ChecksumAddress] = None,
    ) -> PendleSwap:
        """
        Retrieves pricing and transaction data needed to swap between two tokens in a given Pendle market.

        :param sell_token: The token to be sold.
        :param buy_token: The token to be bought.
        :param sell_amount: The amount of sell token to be sold.
        :param slippage: The acceptable slippage percentage for the swap, represented in float terms like 0.01 == 1%
        :param pendle_market: The Pendle market address where the swap will occur.
        :param recipient: The address that will receive the bought tokens. If not provided, the wallet attached to EulithWeb3 will be used.

        :return: A PendleSwap object representing the executed swap.
        """

        try:
            result = self.ew3.eulith_service.pendle_swap(
                sell_token, buy_token, sell_amount, slippage, pendle_market, recipient
            )

            wallet_address = cast(str, self.ew3.wallet_address)
            if wallet_address:
                result["tx"]["from"] = wallet_address
            else:
                # The server returns None in the 'from' field.
                # If we can't set it, we pop it out to avoid serialization issues with a None value
                result["tx"].pop("from")

            return PendleSwap(self.ew3, result)
        except KeyError as e:
            raise EulithRpcException(
                f"the server responded with a payload that didnt have the expected keys (tx), err {e}"
            )
