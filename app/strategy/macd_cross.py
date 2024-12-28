from typing import List, Optional

import pandas as pd

from app.strategy._strategy import BaseStrategy


class MACDCrossStrategy(BaseStrategy):
    """MACD金叉策略"""

    def __init__(self):
        super().__init__(name="MACD金叉", description="MACD金叉买入,死叉卖出")

    async def analyze(self, data: pd.DataFrame) -> List[str]:
        """分析数据"""
        # 判断金叉
        cross_up = (data["diff"] > data["dea"]) & (
            data["diff"].shift(1) <= data["dea"].shift(1)
        )

        # 获取金叉股票
        signals = data[cross_up]
        return signals["code"].tolist()

    async def get_buy_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取买入信号"""
        df = await self.get_stock_data(code, date)
        if df.empty:
            return False

        # 判断最新一天是否金叉
        return (
            df["diff"].iloc[-1] > df["dea"].iloc[-1]
            and df["diff"].iloc[-2] <= df["dea"].iloc[-2]
        )

    async def get_sell_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取卖出信号"""
        df = await self.get_stock_data(code, date)
        if df.empty:
            return False

        # 判断最新一天是否死叉
        return (
            df["diff"].iloc[-1] < df["dea"].iloc[-1]
            and df["diff"].iloc[-2] >= df["dea"].iloc[-2]
        )
