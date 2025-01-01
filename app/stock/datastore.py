from datetime import date
from typing import List, Optional

from sqlalchemy import select

from app.core.database import Base
from app.core.datastore import BaseDatastore
from app.models.stock import (
    StockBlockTrade,
    StockDaily,
    StockIndicator,
    StockLhb,
    StockSignal,
)


class StockDatastore(BaseDatastore[Base]):

    def get_stock_daily(self, code: str, trade_date: date) -> StockDaily:
        """根据股票代码和日期获取数据"""
        st = select(StockDaily).where(
            StockDaily.code == code, StockDaily.trade_date == trade_date
        )
        return self._fetch_one(st)

    def get_stocks_by_date(self, trade_date: date) -> list[StockDaily]:
        """获取某日所有股票数据"""
        st = select(StockDaily).where(StockDaily.trade_date == trade_date)
        return self._fetch_all(st)

    def get_lhb_by_date(self, trade_date: date) -> list[StockLhb]:
        """获取某日龙虎榜数据"""
        st = select(StockLhb).where(StockLhb.trade_date == trade_date)
        return self._fetch_all(st)

    def get_block_trade_by_date(self, trade_date: date) -> list[StockBlockTrade]:
        """获取某日大宗交易数据"""
        st = select(StockBlockTrade).where(StockBlockTrade.trade_date == trade_date)
        return self._fetch_all(st)

    def get_stock_history(
        self, code: str, trade_date: Optional[date] = None
    ) -> list[StockDaily]:
        """获取股票历史数据"""
        query = select(StockDaily).where(StockDaily.code == code)
        if trade_date:
            query = query.where(StockDaily.trade_date >= trade_date)
        return self._fetch_all(query.order_by(StockDaily.trade_date))

    def get_indicator(self, code: str, trade_date: date) -> StockIndicator:
        """获取股票指标数据"""
        st = select(StockIndicator).where(
            StockIndicator.code == code
        ).where(StockIndicator.trade_date == trade_date)
        return self._fetch_one(st)

    def get_indicators_by_date(self, trade_date: date) -> list[StockIndicator]:
        """获取某日所有股票指标"""
        st = select(StockIndicator).where(StockIndicator.trade_date == trade_date)
        return self._fetch_all(st)

    def get_indicator_history(
        self, code: str, trade_date: Optional[date] = None
    ) -> list[StockIndicator]:
        """获取股票指标历史数据"""
        query = select(StockIndicator).where(StockIndicator.code == code)
        if trade_date:
            query = query.where(StockIndicator.trade_date >= trade_date)
        return self._fetch_all(query.order_by(StockIndicator.trade_date))

    def get_signal(self, code: str, trade_date: date) -> Optional[StockSignal]:
        """获取指定日期的股票信号"""
        return self._fetch_one(
            select(StockSignal)
            .where(StockSignal.code == code)
            .where(StockSignal.trade_date == trade_date)
        )

    def get_recent_indicators(
        self,
        code: str,
        trade_date: date,
    ) -> List[StockIndicator]:
        """获取指定日期前N天的指标数据"""
        return self._fetch_all(
            select(StockIndicator)
            .where(StockIndicator.code == code)
            .where(StockIndicator.trade_date >= trade_date)
            .order_by(StockIndicator.trade_date.desc())
        )
