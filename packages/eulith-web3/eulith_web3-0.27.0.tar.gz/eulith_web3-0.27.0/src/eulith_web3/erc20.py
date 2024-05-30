from enum import Enum
from typing import Any, Union, Optional

from eth_typing import ChecksumAddress, Address
from web3.types import TxParams, Wei

from eulith_web3.contract_bindings.i_e_r_c_detailed import IERCDetailed
from eulith_web3.contract_bindings.w_e_t_h_interface import WETHInterface


class TokenSymbol(str, Enum):
    USDT = "USDT"
    BNB = "BNB"
    USDC = "USDC"
    USDCe = "USDC.e"  # in the case of some L2's, this represents the bridged token (instead of Circle's native)
    BUSD = "BUSD"
    MATIC = "MATIC"
    STETH = "stETH"
    WETH = "WETH"
    LDO = "LDO"
    CRV = "CRV"
    CVX = "CVX"
    BAL = "BAL"
    BADGER = "BADGER"
    ONEINCH = "1INCH"
    UNI = "UNI"
    LINK = "LINK"
    APE = "APE"
    GMT = "GMT"
    WBTC = "WBTC"
    LUSD = "LUSD"
    FRAX = "FRAX"
    CBETH = "cbETH"
    GALA = "GALA"
    HEX = "HEX"
    RPL = "RPL"
    DYDX = "DYDX"
    BONE = "BONE"
    LOOKS = "LOOKS"
    AGEUR = "agEUR"
    OSQTH = "oSQTH"
    WSTETH = "wstETH"
    ALBT = "ALBT"
    GLP = "sGLP"
    ARB = "ARB"
    GRT = "GRT"
    FXS = "FXS"
    GMX = "GMX"
    WOO = "WOO"
    COMP = "COMP"


class EulithERC20(IERCDetailed):
    def __init__(
        self,
        eulith_web3: Any,
        contract_address: Optional[Union[Address, ChecksumAddress]] = None,
        decimals: Optional[int] = None,
        symbol: Optional[str] = None,
    ):
        super().__init__(eulith_web3, contract_address)
        self._decimals = decimals
        self._symbol = symbol

    def transfer_float(
        self,
        to: str,
        whole_token_as_float: float,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        return self.transfer(
            to,
            int(whole_token_as_float * 10 ** self.decimals()),
            override_tx_parameters,
        )

    def transfer_from_float(
        self,
        _from: str,
        to: str,
        whole_token_as_float: float,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        return self.transfer_from(
            _from,
            to,
            int(whole_token_as_float * 10 ** self.decimals()),
            override_tx_parameters,
        )

    def approve_float(
        self,
        spender: str,
        whole_token_as_float: float,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        return self.approve(
            spender,
            int(whole_token_as_float * 10 ** self.decimals()),
            override_tx_parameters,
        )

    def allowance_float(self, owner: str, spender: str) -> float:
        return self.allowance(owner, spender) / 10 ** self.decimals()

    def balance_of_float(self, account: str) -> float:
        bal = self.balance_of(account)
        return bal / 10 ** self.decimals()

    def int_to_float(self, x: int) -> float:
        return float(x) / 10 ** self.decimals()

    def float_to_int(self, x: float) -> int:
        return int(x * 10 ** self.decimals())

    def decimals(self) -> int:
        return self._decimals if self._decimals is not None else super().decimals()

    def symbol(self) -> str:
        return self._symbol if self._symbol is not None else super().symbol()


# WETH is special because you can deposit native ETH to the contract to get WETH back
class EulithWETH(WETHInterface, EulithERC20):
    def __init__(
        self,
        eulith_web3: Any,
        contract_address: Optional[Union[Address, ChecksumAddress]] = None,
    ) -> None:
        super().__init__(eulith_web3, contract_address)
        self._decimals = 18
        self._symbol = "WETH"

    def deposit_eth(
        self,
        whole_eth_as_float: float,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        wei = int(whole_eth_as_float * 1e18)  # convert to wei
        return self.deposit_wei(wei, override_tx_parameters)

    def deposit_wei(
        self, wei: int, override_tx_parameters: Optional[TxParams] = None
    ) -> TxParams:
        tx = self.deposit(override_tx_parameters)
        tx["value"] = Wei(wei)
        return tx

    # You must have sufficient WETH balance for this to succeed
    def withdraw_eth(
        self,
        whole_eth_as_float: float,
        override_tx_parameters: Optional[TxParams] = None,
    ) -> TxParams:
        wei = int(whole_eth_as_float * 1e18)
        tx = self.withdraw(wei, override_tx_parameters)
        return tx
