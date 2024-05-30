from typing import Any, Dict, List, Optional, Tuple, Union

from eth_typing import Address, ChecksumAddress
from web3 import Web3
from web3.types import TxParams, TxReceipt, Wei

from eulith_web3.contract_bindings.gmx.i_glp_manager import IGlpManager
from eulith_web3.contract_bindings.gmx.i_order_book import IOrderBook
from eulith_web3.contract_bindings.gmx.i_position_router import IPositionRouter
from eulith_web3.contract_bindings.gmx.i_reader import IReader
from eulith_web3.contract_bindings.gmx.i_reward_router import IRewardRouter
from eulith_web3.contract_bindings.gmx.i_reward_tracker import IRewardTracker
from eulith_web3.contract_bindings.gmx.i_router import IRouter
from eulith_web3.contract_bindings.gmx.i_vault import IVault
from eulith_web3.erc20 import EulithERC20
from eulith_web3.exceptions import EulithRpcException, guard_non_safe_atomic


class GMXV1Position:
    """
    A class that represents a GMX position.

    :param from_dict: A dictionary that contains position data from the Eulith server.

    :ivar collateral_token_address: The address of the collateral token.
    :ivar index_token_address: The address of the index token.
    :ivar is_long: True if the position is long, False if it is short.
    :ivar position_size_denom_usd: The size of the position in USD.
    :ivar collateral_size_denom_usd: The size of the collateral in USD.
    :ivar entry_price_denom_usd: The entry price of the position in USD.
    :ivar realized_pnl: The realized profit and loss of the position in USD.
    :ivar has_profit: True if the position has profit, False otherwise.
    :ivar liquidation_price_denom_usd: The liquidation price of the position in USD.
    :ivar current_delta_denom_usd: The current delta of the position in USD.
    """

    def __init__(self, from_dict: Dict[Any, Any]) -> None:
        """
        :param from_dict: A dictionary that contains position data from the Eulith server.
        """
        self.collateral_token_address: Optional[str] = None
        self.index_token_address: Optional[str] = None
        self.is_long: Optional[bool] = None
        self.position_size_denom_usd: Optional[float] = None
        self.collateral_size_denom_usd: Optional[float] = None
        self.entry_price_denom_usd: Optional[float] = None
        self.realized_pnl: Optional[float] = None
        self.has_profit: Optional[bool] = None
        self.liquidation_price_denom_usd: Optional[float] = None
        self.current_delta_denom_usd: Optional[float] = None

        for key, val in from_dict.items():
            setattr(self, key, val)


class GmxV1Client:
    def __init__(self, ew3: Any) -> None:
        """
        :type ew3: EulithWeb3
        """
        self.addresses = None
        self.price_precision_decimals = 30
        self.ew3 = ew3

    def get_address(self, address_key: str) -> str:
        if self.addresses is None:
            self.addresses = self.ew3.v0.get_gmx_addresses()

        return self.addresses.get(address_key, "")  # type: ignore

    def get_router(self) -> IRouter:
        """
        Gets an instance of `IRouter` that provides access to the GMX Router Contract.
        """
        router_address = self.ew3.to_checksum_address(self.get_address("router"))
        gmx_router = IRouter(self.ew3, router_address)
        return gmx_router

    def get_vault(self) -> IVault:
        """
        Gets an instance of `IVault` that provides access to the GMX Vault Contract.
        """
        vault_address = self.ew3.to_checksum_address(self.get_address("vault"))
        vault = IVault(self.ew3, vault_address)
        return vault

    def get_reader(self) -> IReader:
        """
        Gets an instance of `IReader` that provides access to the GMX Reader Contract.
        """
        reader_address = self.ew3.to_checksum_address(self.get_address("reader"))
        reader = IReader(self.ew3, reader_address)
        return reader

    def get_reward_tracker(self) -> IRewardTracker:
        """
        Gets an instance of `IRewardTracker` that provides access to the GMX RewardTracker contract.
        """
        reward_tracker_address = self.ew3.to_checksum_address(
            self.get_address("reward_tracker")
        )
        reward_tracker = IRewardTracker(self.ew3, reward_tracker_address)
        return reward_tracker

    def get_position_router(self) -> IPositionRouter:
        """
        Returns an instance of the `IPositionRouter` that provides access to the GMX PositionRouter contract.
        """
        position_router_address = self.ew3.to_checksum_address(
            self.get_address("position_router")
        )
        pr = IPositionRouter(self.ew3, position_router_address)
        return pr

    def get_reward_router(self) -> IRewardRouter:
        """
        Returns an instance of the `IRewardRouter` that provides access to the GMX RewardRouter contract.
        """
        rra = self.ew3.to_checksum_address(self.get_address("reward_router"))
        rr = IRewardRouter(self.ew3, rra)
        return rr

    def get_glp_manager(self) -> IGlpManager:
        """
        Returns an instance of the `IGlpManager` that provides access to the GMX GLPManager contract.
        """
        glp_manager_address = self.ew3.to_checksum_address(
            self.get_address("glp_manager")
        )
        gm = IGlpManager(self.ew3, glp_manager_address)
        return gm

    def get_orderbook(self) -> IOrderBook:
        """
        Returns an instance of the `IOrderBook` that provides access to the GMX OrderBook contract.
        """
        ob_address = self.ew3.to_checksum_address(self.get_address("orderbook"))
        ob = IOrderBook(self.ew3, ob_address)
        return ob

    def get_dollar_denominated_token_amt(self, token: EulithERC20, amount: float) -> float:
        """
        Get the dollar-denominated amount of a given token amount on GMX.

        :param token: The token to convert.
        :param amount: The amount of the token to convert.
        :return: The dollar-denominated value of the token, returned in whole float units.
        """
        vault = self.get_vault()
        full_int_amount = int(amount * 10 ** token.decimals())
        token_usd_min = vault.token_to_usd_min(_ensure_address(token.address), full_int_amount)
        return token_usd_min / 10**self.price_precision_decimals

    def ensure_approved_plugin(self, plugin_address: ChecksumAddress) -> Optional[str]:
        """
        Ensures the specified plugin is approved by the GMX router. If not, it sends a transaction to approve it.

        :param plugin_address: The address of the plugin to be approved.
        :return: The hexadecimal representation of the transaction hash if approval was necessary.
        """
        gmx_router = self.get_router()

        if not gmx_router.approved_plugins(self.ew3.wallet_address, plugin_address):
            approve_plugin_tx = gmx_router.approve_plugin(
                plugin_address, {"from": self.ew3.wallet_address, "gas": 5000000}
            )
            h = self.ew3.eth.send_transaction(approve_plugin_tx)
            if not self.ew3.is_atomic():
                self.ew3.eth.wait_for_transaction_receipt(h)

            return h.hex()
        else:
            return None

    def ensure_approved_position_router_plugin(self) -> Optional[str]:
        """
        Ensures that the PositionRouter contract is an approved plugin on the router for the current wallet address.

        :return: A string representing the transaction hash of the approval transaction, if a new approval was required.
        """
        pr = self.get_position_router()
        return self.ensure_approved_plugin(_ensure_address_checksum(pr.address))

    def ensure_approved_orderbook_plugin(self) -> Optional[str]:
        """
        Ensures the orderbook plugin is approved by the GMX router. If not, it sends a transaction to approve it.

        :return: The hexadecimal representation of the transaction hash if approval was necessary.
        """
        ob = self.get_orderbook()
        return self.ensure_approved_plugin(_ensure_address_checksum(ob.address))

    def get_max_ask_price(self, token: EulithERC20) -> float:
        """
        Get the maximum ask price for the given token in USD.

        :param token: An instance of the EulithERC20 class representing the token.
        :return: The maximum ask price in USD.
        """
        vault = self.get_vault()
        max_price = vault.get_max_price(_ensure_address(token.address))
        return max_price / 10**self.price_precision_decimals

    def get_min_bid_price(self, token: EulithERC20) -> float:
        """
        Returns the minimum bid price for a given token.

        :param token: An instance of the EulithERC20 class representing the token.
        :return: The minimum bid price for the given token in USD
        """
        vault = self.get_vault()
        min_price = vault.get_min_price(_ensure_address(token.address))
        return min_price / 10**self.price_precision_decimals

    def get_positions(
        self,
        wallet: ChecksumAddress,
        collateral_tokens: List[EulithERC20],
        index_tokens: List[EulithERC20],
        is_long: List[bool],
    ) -> List[GMXV1Position]:
        """
        Returns a list of GMXPosition objects representing the positions for the specified wallet.
        The returned list matches the order of the collateral_token, index_token, and is_long tuples
        passed in their respective lists.

        :param wallet: The Ethereum wallet address to get the positions for.
        :param collateral_tokens: A list of EulithERC20 tokens that the positions are collateralized with.
        :param index_tokens: A list of EulithERC20 tokens that the positions track.
        :param is_long: A list of boolean values indicating whether the positions are long or short.
        :return: A list of GMXPosition objects representing the positions for the specified wallet.
        """
        result = self.ew3.eulith_service.get_gmx_positions(
            wallet, collateral_tokens, index_tokens, is_long
        )
        positions = result.get("positions", [])
        return_positions = []
        for p in positions:
            return_positions.append(GMXV1Position(p))

        return return_positions

    def mint_glp(
        self, pay_in: EulithERC20, pay_amount: float, slippage: Optional[float] = None
    ) -> Tuple[float, float, List[TxParams]]:
        """
        Mint and stake GLP tokens for a given token and amount.

        :param pay_in: The token to pay with.
        :param pay_amount: The amount of the token to pay with.
        :param slippage: Optional slippage in percentage units i.e. slippage = 0.01 == 1%.
        :return: A tuple of minimum GLP, minimum USD value, and a list of transactions to be executed.
        """
        result = self.ew3.eulith_service.request_gmx_mint_glp(
            pay_in, pay_amount, slippage
        )
        if len(result) > 0:
            r = result[0]
            txs = r.get("txs")
            for t in txs:
                t["from"] = self.ew3.wallet_address
            min_usd_value = r.get("min_usd_value")
            min_glp = r.get("min_glp")
            return min_glp, min_usd_value, txs
        else:
            raise EulithRpcException("mint and stake glp returned empty list response")

    def redeem_glp(
        self,
        receive_token: EulithERC20,
        glp_amount: float,
        min_receive_token: Optional[float] = None,
        receiving_address: Optional[ChecksumAddress] = None,
    ) -> TxParams:
        """
        Redeems GLP tokens for an equivalent value of `receive_token`.

        :param receive_token: The token to receive in exchange for GLP.
        :param glp_amount: The amount of GLP tokens to redeem.
        :param min_receive_token: The minimum amount of `receive_token` to receive.
        :param receiving_address: The address to receive the `receive_token`. Defaults to the current wallet address.
        :return: A dictionary containing transaction parameters.
        """
        rr = self.get_reward_router()
        glp_amount_int = int(glp_amount * 10**18)
        min_receive_int = int(min_receive_token * 10 ** receive_token.decimals())

        if not receiving_address:
            receiving_address = self.ew3.wallet_address

        tx = rr.unstake_and_redeem_glp(
            _ensure_address(receive_token.address),
            glp_amount_int,
            min_receive_int,
            _ensure_address(receiving_address),
            {"from": self.ew3.wallet_address, "gas": 1500000},
        )

        return tx

    def get_dollar_denom_glp_value(self) -> float:
        """
        Get the dollar-denominated value of one GLP.

        :return: The dollar-denominated value of one GLP.
        """
        glp_manager = self.get_glp_manager()
        price = glp_manager.get_price(False)
        return price / 10**self.price_precision_decimals

    def get_staked_glp_balance(self, wallet_address: ChecksumAddress) -> float:
        """
        Get the amount of staked GLP for the given wallet address.

        :param wallet_address: The wallet address to check the staked GLP balance for.
        :return: The amount of staked GLP for the given wallet address.
        """
        reward_tracker = self.get_reward_tracker()
        balance = reward_tracker.balance_of(wallet_address)
        return balance / 10**18  # 18 magic number here is the token decimal value

    # The fee is whole units denominated in the buy_token. For example on a swap from WETH to USDC, fee = 0.04
    # means 0.04 USDC is being taken as a fee
    # Swap fees are 0.2% - 0.8% https://gmxio.gitbook.io/gmx/trading
    def swap(
        self,
        sell_token: EulithERC20,
        buy_token: EulithERC20,
        amount_in: float,
        slippage: float = 0.01,
        recipient: Optional[ChecksumAddress] = None,
        approve_erc: bool = False,
    ) -> Tuple[float, float, TxParams]:
        """
        Executes a swap between two tokens using the current router.

        :param sell_token: The token to sell.
        :param buy_token: The token to buy.
        :param amount_in: The amount of sell_token to sell in whole float units.
        :param slippage: The acceptable slippage for the trade, expressed as decimal percentage defaults to 0.01 == 1%
        :param recipient: The address to send the purchased tokens to. Defaults to the calling wallet address.
        :param approve_erc: If True, do the necessary pre-requisite ERC20 approvals automatically
        :return: A tuple of the swap price, fee amount and transaction parameters.
                 The fee is whole units denominated in the buy_token
        """
        router = self.get_router()
        reader = self.get_reader()
        vault = self.get_vault()

        amount_in_int = int(amount_in * 10 ** sell_token.decimals())

        router_allowance = sell_token.allowance_float(
            self.ew3.wallet_address, _ensure_address(router.address)
        )

        if approve_erc and router_allowance < amount_in:
            self._approve_erc(amount_in - router_allowance, sell_token)

        out_amount, fee = reader.get_amount_out(
            vault.address, _ensure_address(sell_token.address), _ensure_address(buy_token.address), amount_in_int
        )
        out_amount_float = out_amount / 10 ** buy_token.decimals()

        min_amount_out = int((1 - slippage) * out_amount)

        if not recipient:
            recipient = self.ew3.wallet_address

        tx_params = router.swap(
            [_ensure_address(sell_token.address), _ensure_address(buy_token.address)],
            amount_in_int,
            min_amount_out,
            _ensure_address(recipient),
            {"from": self.ew3.wallet_address, "gas": 2000000},
        )

        price = amount_in / out_amount_float

        float_fee = fee / 10 ** buy_token.decimals()

        return price, float_fee, tx_params

    def create_increase_order(
        self,
        position_token: EulithERC20,
        pay_token: EulithERC20,
        true_for_long: bool,
        amount_in: float,
        size_delta_usd: float,
        limit_price_usd: float,
        approve_erc: bool = True,
    ) -> Optional[TxReceipt]:
        """
        Creates an increase order (buy limit order) for a given position token, paid with a specified pay token.

        :param position_token: The token for which the position will be increased.
        :param pay_token: The token to be used for payment.
        :param true_for_long: True for a long position, false for a short one.
        :param amount_in: The amount of pay token to be used.
        :param size_delta_usd: The change in position size in USD (whole float values i.e. 1.0 = 1 USD).
        :param limit_price_usd: The limit price in USD for the order. The order will execute at or below this price (for long positions).
        :param approve_erc: If True, approves the ERC20 token for the transaction.
        :return: The transaction receipt if the order was created successfully.
        """

        guard_non_safe_atomic(self.ew3)

        self.ensure_approved_orderbook_plugin()

        ob = self.get_orderbook()
        amount_in_int = pay_token.float_to_int(amount_in)

        size_delta_int = int(size_delta_usd * 10**self.price_precision_decimals)

        limit_price_int = limit_price_usd * 10**self.price_precision_decimals

        pr = self.get_position_router()
        fee = pr.min_execution_fee()

        if approve_erc:
            self._approve_erc(amount_in_int, pay_token)

        path = [_ensure_address(pay_token.address)]

        trigger_above_threshold = not true_for_long

        order_tx = ob.create_increase_order(
            path,
            amount_in_int,
            _ensure_address(position_token.address),
            0,
            size_delta_int,
            _ensure_address(position_token.address),
            true_for_long,
            limit_price_int,
            trigger_above_threshold,
            fee,
            False,
            {"from": self.ew3.wallet_address, "gas": 20000000, "value": Wei(fee)},
        )

        return self._send_and_wait_if_not_atomic(order_tx)

    def create_decrease_order(
        self,
        position_token: EulithERC20,
        collateral_token: EulithERC20,
        size_delta_usd: float,
        collateral_delta_usd: float,
        true_for_long: bool,
        limit_price_usd: float,
    ) -> Optional[TxReceipt]:
        """
        Creates a decrease order (sell limit order) for a given position/collateral pair. In most cases, the collateral
        token will be the same as the permission token unless you specifically have an otherwise collateralized position.

        :param position_token: The token for which the position will be decreased.
        :param collateral_token: The collateral token to be decreased by `collateral_delta_usd`
        :param size_delta_usd: The size delta in USD for the position.
        :param collateral_delta_usd: The collateral delta in USD for the position.
        :param true_for_long: True for a long position, false for a short one.
        :param limit_price_usd: The limit price in USD for the order. The order will be executed at or above this price (for long positions).
        :return: The transaction receipt if the order was created successfully.
        """

        guard_non_safe_atomic(self.ew3)

        size_delta_int = int(size_delta_usd * 10**self.price_precision_decimals)
        collateral_delta_int = int(
            collateral_delta_usd * 10**self.price_precision_decimals
        )

        limit_price_int = int(limit_price_usd * 10**self.price_precision_decimals)

        trigger_above_threshold = true_for_long

        self.ensure_approved_orderbook_plugin()

        ob = self.get_orderbook()

        pr = self.get_position_router()
        fee = pr.min_execution_fee()

        order_tx = ob.create_decrease_order(
            _ensure_address(position_token.address),
            size_delta_int,
            _ensure_address(collateral_token.address),
            collateral_delta_int,
            true_for_long,
            limit_price_int,
            trigger_above_threshold,
            {"from": self.ew3.wallet_address, "gas": 5000000, "value": Wei(fee)},
        )

        return self._send_and_wait_if_not_atomic(order_tx)

    def increase_position(
        self,
        position_token: EulithERC20,
        collateral_token: EulithERC20,
        true_for_long: bool,
        collateral_amount_in: float,
        leverage: float = 1.0,
        approve_erc: bool = True,
    ) -> Optional[TxReceipt]:
        """
        Increases a GMX position.

        :param position_token: The position token to be manipulated.
        :param collateral_token: The token to use for collateral.
        :param true_for_long: If True, the position is a long position. Otherwise, it is a short position.
        :param collateral_amount_in: The amount of collateral to add to the position.
        :param leverage: The leverage to use. Default is 1.0.
        :param approve_erc: If True, do the necessary pre-requisite ERC20 approvals automatically
        :return: If successful, returns a transaction receipt. Otherwise, returns None.
        """
        self.ensure_approved_position_router_plugin()

        token_usd_min = int(
            self.get_dollar_denominated_token_amt(
                collateral_token, collateral_amount_in
            )
            * 10**self.price_precision_decimals
            * leverage
        )

        full_int_amount = int(collateral_amount_in * 10 ** collateral_token.decimals())

        pr = self.get_position_router()
        fee = pr.min_execution_fee()

        increase_position_path = [_ensure_address(collateral_token.address)]
        zero_address = "0x0000000000000000000000000000000000000000"

        if true_for_long:
            acceptable_price = int(
                self.get_max_ask_price(position_token)
                * 10**self.price_precision_decimals
            )
        else:
            acceptable_price = int(
                self.get_min_bid_price(position_token)
                * 10**self.price_precision_decimals
            )

        if approve_erc:
            self._approve_erc(collateral_amount_in, collateral_token)

        increase_position_tx = pr.create_increase_position(
            increase_position_path,
            _ensure_address(position_token.address),
            full_int_amount,
            0,
            token_usd_min,
            true_for_long,
            acceptable_price,
            fee,
            b"00000000000000000000000000000000",
            zero_address,
            {"from": self.ew3.wallet_address, "gas": 5000000, "value": Wei(fee)},
        )

        return self._send_and_wait_if_not_atomic(increase_position_tx)

    def decrease_position(
        self,
        position_token: EulithERC20,
        collateral_token: EulithERC20,
        true_for_long: bool,
        decrease_collateral: float,
        decrease_exposure: float,
        recipient: Optional[str] = None,
    ) -> Optional[TxReceipt]:
        """
        Decreases an existing position.

        :param position_token: The position token to decrease.
        :param collateral_token: The collateral token.
        :param true_for_long: True if the position is long, False if short.
        :param decrease_collateral: The amount of collateral to decrease.
        :param decrease_exposure: The amount of position token to decrease.
        :param recipient: The address to receive the returned tokens. Defaults to the wallet address.
        :return: The transaction receipt if the transaction was successful, otherwise None.
        """
        self.ensure_approved_position_router_plugin()

        collateral_change = int(
            self.get_dollar_denominated_token_amt(collateral_token, decrease_collateral)
            * 10**self.price_precision_decimals
        )

        size_change = int(
            self.get_dollar_denominated_token_amt(position_token, decrease_exposure)
            * 10**self.price_precision_decimals
        )

        pr = self.get_position_router()
        fee = pr.min_execution_fee()

        decrease_path = [_ensure_address(collateral_token.address)]
        zero_address = "0x0000000000000000000000000000000000000000"

        if true_for_long:
            acceptable_price = int(
                self.get_max_ask_price(position_token)
                * 10**self.price_precision_decimals
            )
        else:
            acceptable_price = int(
                self.get_min_bid_price(position_token)
                * 10**self.price_precision_decimals
            )

        if not recipient:
            recipient = self.ew3.wallet_address

        decrease_position_tx = pr.create_decrease_position(
            decrease_path,
            _ensure_address(position_token.address),
            collateral_change,
            size_change,
            true_for_long,
            recipient,  # type: ignore
            acceptable_price,
            0,
            fee,
            False,
            zero_address,
            {"from": self.ew3.wallet_address, "gas": 5000000, "value": Wei(fee)},
        )

        return self._send_and_wait_if_not_atomic(decrease_position_tx)

    def _approve_erc(self, amount_in: float, input_token: EulithERC20) -> None:
        router_address = self.ew3.to_checksum_address(self.get_address("router"))
        at = input_token.approve_float(
            router_address, amount_in, {"from": self.ew3.wallet_address, "gas": 2000000}
        )
        h = self.ew3.eth.send_transaction(at)
        if not self.ew3.is_atomic():
            self.ew3.eth.wait_for_transaction_receipt(h)

    def _send_and_wait_if_not_atomic(self, order_tx: Any) -> Optional[TxReceipt]:
        h = self.ew3.eth.send_transaction(order_tx)
        if not self.ew3.is_atomic():
            r = self.ew3.eth.wait_for_transaction_receipt(h)
            return r
        else:
            return None


def _ensure_address_checksum(address: Union[Address, ChecksumAddress, None]) -> ChecksumAddress:
    if address is None:
        raise ValueError("address is None")

    if isinstance(address, bytes):
        # address is Address
        return Web3.to_checksum_address(address)
    else:
        # address is ChecksumAddress
        return address


def _ensure_address(address: Union[Address, ChecksumAddress, None]) -> str:
    return str(_ensure_address_checksum(address))
