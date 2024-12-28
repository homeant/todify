from typing import List, Optional

import pandas as pd

from app.strategy._strategy import BaseStrategy


class KDJStrategy(BaseStrategy):
    """KDJ超买超卖策略"""

    def __init__(self):
        super().__init__(name="KDJ超买超卖", description="KDJ超卖买入,超买卖出")
        self.oversold = 20  # 超卖线
        self.overbought = 80  # 超买线

    async def analyze(self, data: pd.DataFrame) -> List[str]:
        """分析数据"""
        # 判断超卖
        oversold = (data["k"] < self.oversold) & (data["d"] < self.oversold)

        # 获取超卖股票
        signals = data[oversold]
        return signals["code"].tolist()

    async def get_buy_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取买入信号"""
        df = await self.get_stock_data(code, date)
        if df.empty:
            return False

        # 判断是否超卖
        return df["k"].iloc[-1] < self.oversold and df["d"].iloc[-1] < self.oversold

    async def get_sell_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取卖出信号"""
        df = await self.get_stock_data(code, date)
        if df.empty:
            return False

        # 判断是否超买
        return df["k"].iloc[-1] > self.overbought and df["d"].iloc[-1] > self.overbought
