from datetime import datetime

import akshare as ak
import arrow

from app.core.singleton import Singleton


class TradeCalendar(metaclass=Singleton):
    """交易日历类，用于处理交易时间相关的判断"""

    def __init__(self):
        self._init_trade_calendar()

    def _init_trade_calendar(self):
        """初始化交易日历数据，从新浪接口获取实际的交易日历"""
        try:
            self._update_trade_calendar()
        except Exception as e:
            raise e

    def _update_trade_calendar(self):
        """更新交易日历数据"""
        trade_date_df = ak.tool_trade_date_hist_sina()
        # 将日期转换为Arrow对象
        self.trade_days = [arrow.get(str(date)) for date in trade_date_df["trade_date"]]
        self.last_update_time = arrow.now()

    def _check_and_update_calendar(self):
        """检查是否需要更新交易日历"""
        if not hasattr(self, "trade_days") or not self.trade_days:
            self._update_trade_calendar()
            return

        today = arrow.now()
        if self.trade_days[-1] <= today.shift(days=5):
            self._update_trade_calendar()

    def is_trade_day(self, date=None):
        """判断是否为交易日"""
        self._check_and_update_calendar()
        if date is None:
            date = arrow.now()
        elif isinstance(date, datetime):
            date = arrow.get(date)
        return date.floor("day") in [d.floor("day") for d in self.trade_days]

    def get_next_trade_day(self, date=None):
        """获取下一个交易日

        Args:
            date: datetime 或 arrow 对象，默认为当前时间
        Returns:
            arrow: 下一个交易日，如果没有则返回 None
        """
        self._check_and_update_calendar()
        if date is None:
            date = arrow.now()
        elif isinstance(date, datetime):
            date = arrow.get(date)

        next_days = [d for d in self.trade_days if d > date]
        return next_days[0] if next_days else None

    def get_previous_trade_day(self, date=None):
        """获取上一个交易日

        Args:
            date: datetime 或 arrow 对象，默认为当前时间
        Returns:
            arrow: 上一个交易日，如果没有则返回 None
        """
        self._check_and_update_calendar()
        if date is None:
            date = arrow.now()
        elif isinstance(date, datetime):
            date = arrow.get(date)

        prev_days = [d for d in self.trade_days if d < date]
        return prev_days[-1] if prev_days else None

    def get_last_trade_day(self) -> arrow.Arrow:
        """获取最后一个交易日（不超过今天）

        Returns:
            arrow: 最后一个交易日，如果没有则返回 None
        """
        self._check_and_update_calendar()
        today = arrow.now()
        valid_days = [day for day in self.trade_days if day <= today]
        return valid_days[-1] if valid_days else None
