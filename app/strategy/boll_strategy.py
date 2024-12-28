from typing import List, Optional

import pandas as pd

from app.strategy._strategy import BaseStrategy


class BollStrategy(BaseStrategy):
    """布林带策略"""

    def __init__(self):
        super().__init__(
            name="布林带交易", description="价格突破布林上轨卖出,跌破下轨买入"
        )

    async def analyze(self, data: pd.DataFrame) -> List[str]:
        """分析数据"""
        # 获取突破下轨的股票
        break_down = (data["close"] < data["boll_down"]) & (
            data["close"].shift(1) >= data["boll_down"].shift(1)
        )

        # 返回买入信号股票
        signals = data[break_down]
        return signals["code"].tolist()

    async def get_buy_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取买入信号"""
        df = await self.get_stock_data(code, date)
        if df.empty:
            return False

        # 判断是否跌破下轨
        return (
            df["close"].iloc[-1] < df["boll_down"].iloc[-1]
            and df["close"].iloc[-2] >= df["boll_down"].iloc[-2]
        )

    def get_sell_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取卖出信号"""
        df = self.service.get_history_data(code)
        if df.empty:
            return False

        # 判断是否突破上轨
        return (
            df["close"].iloc[-1] > df["boll_up"].iloc[-1]
            and df["close"].iloc[-2] <= df["boll_up"].iloc[-2]
        )
