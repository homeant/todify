from datetime import date
from typing import Optional

from sqlalchemy import select

from app.core.database import Base
from app.core.datastore import BaseDatastore
from app.models.stock import StockBlockTrade, StockDaily, StockIndicator, StockLhb


class StockDatastore(BaseDatastore[Base]):

    def get_stock_by_code_and_date(self, code: str, trade_date: date) -> StockDaily:
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
            StockIndicator.code == code, StockIndicator.trade_date == trade_date
        )
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
