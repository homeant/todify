from typing import List, Optional

import pandas as pd

from app.stock.data_service import StockDataService
from app.strategy.base import BaseStrategy


class DMIStrategy(BaseStrategy):
    """DMI趋势策略"""

    def __init__(self):
        super().__init__(
            name="DMI趋势", description="PDI上穿MDI买入,下穿卖出,ADX确认趋势"
        )
        self.service = StockDataService()
        self.adx_threshold = 25  # ADX趋势确认阈值

    def analyze(self, data: pd.DataFrame) -> List[str]:
        """分析数据"""
        # PDI上穿MDI且ADX大于阈值
        cross_up = (
            (data["pdi"] > data["mdi"])
            & (data["pdi"].shift(1) <= data["mdi"].shift(1))
            & (data["adx"] > self.adx_threshold)
        )

        signals = data[cross_up]
        return signals["code"].tolist()

    def get_buy_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取买入信号"""
        df = self.service.get_history_data(code)
        if df.empty:
            return False

        return (
            df["pdi"].iloc[-1] > df["mdi"].iloc[-1]
            and df["pdi"].iloc[-2] <= df["mdi"].iloc[-2]
            and df["adx"].iloc[-1] > self.adx_threshold
        )

    def get_sell_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取卖出信号"""
        df = self.service.get_history_data(code)
        if df.empty:
            return False

        return (
            df["pdi"].iloc[-1] < df["mdi"].iloc[-1]
            and df["pdi"].iloc[-2] >= df["mdi"].iloc[-2]
        )
