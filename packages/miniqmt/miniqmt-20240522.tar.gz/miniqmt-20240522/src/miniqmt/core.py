"""miniQMT adapter for VXQuant API"""

import logging
import time
from pathlib import Path
from typing import Union, Optional, Dict, Any, List, Literal
from xtquant import xtdata
from xtquant import xtconstant
from xtquant.xttype import (
    StockAccount,
    XtAsset,
    XtAccountStatus,
    XtPosition,
    XtOrder,
    XtTrade,
    XtOrderError,
    XtCancelError,
)
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from miniqmt.adapters import (
    miniqmt_order_adapter,
    miniqmt_execrpt_adapter,
    miniqmt_position_adapter,
    miniqmt_tick_adapter,
    miniqmt_cashinfo_adapter,
)
from vxquant.models.preset import VXMarketPreset
from vxquant.models.nomalize import to_symbol
from vxquant.models.base import VXTick, VXOrder, VXPosition, VXExecRpt, VXCashInfo
from vxutils.datamodel.dborm import VXDataBase, VXDBSession
from vxutils import retry
from vxsched import vxsched

xtdata.enable_hello = False


class VXMiniQMTTDAPI(XtQuantTraderCallback):
    def __init__(
        self,
        path: Union[str, Path],
        account_id: str,
        acount_type: str = "STOCK",
        db_uri: str = "",
    ) -> None:
        self._xt_trader: Optional[XtQuantTrader] = None
        self._path = path
        self._account = StockAccount(
            account_id=account_id, account_type=acount_type.upper()
        )
        self._db = self.init_db(db_uri)
        # xtdata.subscribe_whole_quote(["SH", "SZ"], self.on_price_update)

    def init_db(self, db_uri: str) -> VXDataBase:
        db = VXDataBase(db_uri)
        db.create_table("ticks", ["symbol"], VXTick, if_exists="ignore")
        return db

    def on_price_update(self, qmt_ticks: Dict[str, Any]) -> None:
        """_summary_

        Arguments:
            qmt_ticks {Dict[str, Any]} -- 收到的行情数据更新
        """
        with self._db.start_session() as session:
            start = time.perf_counter()
            for stock_code, qmt_tick in qmt_ticks.items():
                qmt_tick["stock_code"] = stock_code
                session.save("ticks", miniqmt_tick_adapter(qmt_tick))
            logging.info(f"Saved {len(qmt_ticks)} ticks to database...")

    @property
    @retry(3, (RuntimeError, ConnectionError, TimeoutError), delay=0.3, backoff=2)
    def trader(self) -> XtQuantTrader:
        if self._xt_trader:
            return self._xt_trader

        self._xt_trader = XtQuantTrader(self._path, int(time.time()), callback=self)
        self._xt_trader.start()
        connect_result = self._xt_trader.connect()
        if connect_result != 0:
            raise ConnectionError(
                f"Failed to start XtQuantTrader, connect error_code: {connect_result}"
            )
        logging.info("XtQuantTrader started successfully...")

        subscribe_result = self._xt_trader.subscribe(self._account)
        if subscribe_result != 0:
            raise RuntimeError(
                f"Failed to subscribe account, subscribe error_code: {subscribe_result}"
            )
        logging.info(f"Account[{self._account.account_id}] subscribed successfully...")
        return self._xt_trader

    def current(self, *symbols: str) -> Dict[str, VXTick]:
        ticks = xtdata.get_full_tick(symbols)
        datas = {}
        for stock_code, tick in ticks.items():
            tick["stock_code"] = stock_code
            datas[stock_code] = miniqmt_tick_adapter(tick)
        return datas

    def get_positions(self, symbol: str = "") -> Dict[str, VXPosition]:
        positions = self.trader.query_stock_positions(self._account)
        return dict(
            miniqmt_position_adapter(pos, key="symbol")
            for pos in positions
            if pos.volume > 0
        )

    def get_orders(
        self, order_id: str = "", is_open: bool = True
    ) -> Dict[str, VXOrder]:
        orders = self.trader.query_stock_orders(
            self._account, cancelable_only=(not is_open)
        )
        return dict(miniqmt_order_adapter(order, key="order_id") for order in orders)

    def get_trades(self, trade_id: str = "") -> Dict[str, VXExecRpt]:
        trades = self.trader.query_stock_trades(self._account)
        return dict(
            miniqmt_execrpt_adapter(trade, key="execrpt_id") for trade in trades
        )

    def get_cash(self) -> VXCashInfo:
        cash = self.trader.query_stock_asset(self._account)
        return miniqmt_cashinfo_adapter(cash)

    def order_batch(self, *orders: VXOrder) -> List[VXOrder]:
        for order in orders:
            order_id = self.trader.order_stock(
                self._account,
                order.symbol,
                order_type=(
                    xtconstant.STOCK_BUY
                    if order.order_side.name == "Buy"
                    else xtconstant.STOCK_SELL
                ),
                order_volume=order.volume,
                price_type=(
                    xtconstant.FIX_PRICE
                    if order.order_type.name == "Limit"
                    else xtconstant.MARKET_PEER_PRICE_FIRST
                ),
                price=order.price,
                strategy_name=order.strategy_id,
                order_remark=order.order_remark,
            )
            order.order_id = str(order_id)

        return list(orders)

    def order_volume(
        self,
        symbol: str,
        volume: int,
        price: Optional[float] = None,
        order_remark: str = "",
        strategy_id: str = "",
    ) -> VXOrder:
        """下单函数

        Arguments:
            symbol {str} -- 证券代码
            volume {int} -- 下单数量，正数为买，负数为卖
            price {Optional[float]} -- 委托价格 (default: {None})
            order_remark {str} -- 下单备注 (default: {""})
            strategy_id {str} -- 策略ID (default: {""})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        symbol = to_symbol(symbol)
        order_side = "Buy" if volume > 0 else "Sell"
        order_type = (
            "Market"
            if price is None
            and VXMarketPreset(symbol=symbol).security_type.name == "BOND_CONVERTIBLE"
            else "Limit"
        )
        if price is None:
            ticks = xtdata.get_full_tick([symbol])
            price = (
                ticks[symbol]["askPrice"][0]
                if order_side == "Buy"
                else ticks[symbol]["bidPrice"][0]
            )

        order = VXOrder(
            account_id=self._account.account_id,
            symbol=symbol,
            volume=abs(volume),
            price=price,
            order_side=order_side,
            order_type=order_type,
            position_effect="Open" if volume > 0 else "Close",
            order_remark=order_remark,
            strategy_id=strategy_id,
        )

        return self.order_batch(order)[0]

    def order_cancel(self, order: Union[str, VXOrder]) -> None:
        """撤单函数

        Arguments:
            order_id {str} -- 委托订单号
        """

        order_id = order.order_id if isinstance(order, VXOrder) else order
        cancel_result = self.trader.cancel_order_stock(self._account, order_id)
        if cancel_result != 0:
            raise RuntimeError(f"Failed to cancel order: {order_id}")

    def auto_repo(
        self,
        reversed_balance: float = 0.0,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> Optional[VXOrder]:
        """自动回购函数

        Arguments:
            reversed_balance {float} -- 回购金额
            symbols {List[str]} -- 证券代码列表

        Keyword Arguments:
            strategy_id {str} -- 策略ID (default: {""})
            order_remark {str} -- 下单备注 (default: {""})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        cash = self.get_cash()
        if cash.available < reversed_balance:
            raise ValueError("Available cash is not enough for repo...")

        target_repo_balance = cash.available - reversed_balance
        target_repo_volume = int(target_repo_balance // 100 // 10 * 10)
        if target_repo_volume <= 0:
            return None

        if not symbols:
            symbols = ["131810.SZ", "204001.SH"]

        ticks = self.current(*symbols)
        target_repo_symbol = ""
        for symbol in symbols:
            tick = ticks.get(symbol, None)
            if not tick:
                logging.warning(f"Tick data for {symbol} is not available...")
                continue
            if (
                target_repo_symbol == ""
                or tick.ask1_p > ticks[target_repo_symbol].ask1_p
            ):
                target_repo_symbol = symbol
        if target_repo_symbol == "":
            logging.warning("No available tick data for repo...")
            return None

        logging.info(f"Auto repo: {target_repo_symbol} {target_repo_volume}")
        return self.order_volume(
            symbol=symbols[0],
            volume=-target_repo_volume,
            price=ticks[target_repo_symbol].ask1_p,
            order_remark=order_remark,
            strategy_id=strategy_id,
        )

    def auto_ipo_bond_purchase(
        self,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> List[VXOrder]:
        """自动新债申购函数

        Arguments:
            symbols {List[str]} -- 申购证券代码列表，若为空则根据策略自动选择，否则按照列表顺序申购
            strategy_id {str} -- 策略ID
            order_remark {str} -- 交易备注

        Returns:
            List[VXOrder] -- _description_
        """
        ipos = self.trader.query_ipo_data()
        orders = []
        for symbol, info in ipos.items():
            if info["type"] != "BOND":
                continue

            if symbols is None or symbol in symbols:
                order = self.order_volume(
                    symbol=symbol,
                    volume=info["maxPurchaseNum"],
                    price=info["issuePrice"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                orders.append(order)
                logging.info(f"Auto IPO BOND: {symbol} {info}")
        return orders

    def auto_ipo_stock_purchase(
        self,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> List[VXOrder]:
        ipo_limits = self.trader.query_ipo_data(self._account)
        orders = []
        ipos = self.trader.query_ipo_data()
        for symbol, info in ipos.items():
            if info["type"] != "STOCK":
                continue

            if symbols is None or symbol in symbols:
                if symbol.startswith("0"):
                    ipo_limit = ipo_limits["SZ"]
                elif symbol.startswith("787"):
                    ipo_limit = ipo_limits["SH"]
                else:
                    ipo_limit = ipo_limits["KCB"]

                order = self.order_volume(
                    symbol=symbol,
                    volume=min(info["maxPurchaseNum"], ipo_limit),
                    price=info["issuePrice"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                orders.append(order)
                logging.info(f"Auto IPO STOCK: {symbol} {info}")
        return orders

    def on_account_status(self, account_status: XtAccountStatus) -> None:
        if account_status.status == xtconstant.ACCOUNT_STATUS_OK:
            logging.info(f"Account status: {account_status.status}")
        else:
            logging.error(f"Account status error: {account_status.status}")

    def on_disconnected(self) -> None:
        """掉线通知回调函数"""
        logging.error("Disconnected from server... waiting for reconnect...")
        self._xt_trader = None

    def on_stock_asset(self, data: XtAsset) -> None:
        logging.info(f"Stock asset: {data}")

    def on_stock_order(self, data: XtOrder) -> None:
        """委托更新回调函数

        Arguments:
            data {XtOrder} -- 交易订单信息
        """
        order = miniqmt_order_adapter(data)
        logging.info(f"Receive order status updated: {order}")
        vxsched.publish("on_order_status", data=order, channel=self._account.account_id)

    def on_stock_position(self, data: XtPosition) -> None:
        logging.info(f"Stock position: {data}")

    def on_stock_trade(self, data: XtTrade) -> None:
        """成交回报回调函数

        Arguments:
            data {XtTrade} -- 成交信息
        """
        execrpt = miniqmt_execrpt_adapter(data)
        logging.info(f"Receive trade report: {execrpt}")
        vxsched.publish(
            "on_trade_report", data=execrpt, channel=self._account.account_id
        )

    def on_order_error(self, data: XtOrderError) -> None:
        """委托错误回调函数

        Arguments:
            data {XtOrderError} -- 报错信息
        """
        qmt_orders = self.trader.query_stock_orders(self._account)
        for qmt_order in qmt_orders:
            if qmt_order.order_id == data.order_id:
                order = miniqmt_order_adapter(qmt_order)
                order.reject_reason = f"{data.error_id}--{data.error_msg}"
                order.status = "Rejected"
                logging.warning(
                    f"Order {data.order_id} error: {order.error_id}--{order.error_msg}"
                )
                vxsched.publish(
                    "on_order_status", data=order, channel=self._account.account_id
                )
                break

    def on_cancel_error(self, data: XtCancelError) -> None:
        logging.warning(
            f"Order {data.order_id} Cancel error: {data.error_id}--{data.error_msg}"
        )
