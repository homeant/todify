from typing import List, Optional

import pandas as pd

from app.stock.data_service import StockDataService
from app.strategy.base import BaseStrategy


class ComboStrategy(BaseStrategy):
    """多指标组合策略"""

    def __init__(self):
        super().__init__(name="多指标组合", description="MACD金叉+KDJ超卖+成交量放大")
        self.service = StockDataService()
        self.volume_ratio = 2  # 成交量放大倍数
        self.kdj_oversold = 20  # KDJ超卖阈值

    def analyze(self, data: pd.DataFrame) -> List[str]:
        """分析数据"""
        # MACD金叉
        macd_cross = (data["diff"] > data["dea"]) & (
            data["diff"].shift(1) <= data["dea"].shift(1)
        )

        # KDJ超卖
        kdj_oversold = (data["k"] < self.kdj_oversold) & (data["d"] < self.kdj_oversold)

        # 成交量放大
        volume_up = data["volume"] > data["vma5"] * self.volume_ratio

        # 组合信号
        signals = data[macd_cross & kdj_oversold & volume_up]
        return signals["code"].tolist()

    def get_buy_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取买入信号"""
        df = self.service.get_history_data(code)
        if df.empty:
            return False

        # 判断组合条件
        macd_cross = (
            df["diff"].iloc[-1] > df["dea"].iloc[-1]
            and df["diff"].iloc[-2] <= df["dea"].iloc[-2]
        )

        kdj_oversold = (
            df["k"].iloc[-1] < self.kdj_oversold
            and df["d"].iloc[-1] < self.kdj_oversold
        )

        volume_up = df["volume"].iloc[-1] > df["vma5"].iloc[-1] * self.volume_ratio

        return macd_cross and kdj_oversold and volume_up

    def get_sell_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取卖出信号"""
        df = self.service.get_history_data(code)
        if df.empty:
            return False

        # 任一条件触发即卖出
        macd_dead = (
            df["diff"].iloc[-1] < df["dea"].iloc[-1]
            and df["diff"].iloc[-2] >= df["dea"].iloc[-2]
        )

        kdj_overbought = df["k"].iloc[-1] > 80 and df["d"].iloc[-1] > 80

        return macd_dead or kdj_overbought
