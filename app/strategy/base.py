from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd

from app.stock.data_service import StockDataService


class BaseStrategy(ABC):
    """策略基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.service = StockDataService()

    async def get_stock_data(
        self, code: str, date: Optional[str] = None
    ) -> pd.DataFrame:
        """获取股票数据(包含指标)"""
        return await self.service.get_history_with_indicators(code, date)

    @abstractmethod
    async def analyze(self, data: pd.DataFrame) -> List[str]:
        """分析数据并返回符合条件的股票代码列表"""
        pass

    @abstractmethod
    async def get_buy_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取买入信号"""
        pass

    @abstractmethod
    async def get_sell_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取卖出信号"""
        pass
