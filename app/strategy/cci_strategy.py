from typing import List, Optional

import pandas as pd

from app.stock.data_service import StockDataService
from app.strategy.base import BaseStrategy


class CCIStrategy(BaseStrategy):
    """CCI超买超卖策略"""

    def __init__(self):
        super().__init__(name="CCI超买超卖", description="CCI超卖买入,超买卖出")
        self.service = StockDataService()
        self.oversold = -100  # 超卖阈值
        self.overbought = 100  # 超买阈值

    def analyze(self, data: pd.DataFrame) -> List[str]:
        """分析数据"""
        # 超卖反转
        oversold = (data["cci"] > self.oversold) & (
            data["cci"].shift(1) <= self.oversold
        )

        signals = data[oversold]
        return signals["code"].tolist()

    def get_buy_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取买入信号"""
        df = self.service.get_history_data(code)
        if df.empty:
            return False

        return (
            df["cci"].iloc[-1] > self.oversold and df["cci"].iloc[-2] <= self.oversold
        )

    def get_sell_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取卖出信号"""
        df = self.service.get_history_data(code)
        if df.empty:
            return False

        return df["cci"].iloc[-1] > self.overbought
