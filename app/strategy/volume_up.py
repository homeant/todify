from typing import List, Optional

import pandas as pd

from app.stock.data_service import StockDataService
from app.strategy.base import BaseStrategy
from app.utils.indicator import calculate_ma


class VolumeUpStrategy(BaseStrategy):
    """放量上涨策略"""

    def __init__(self):
        super().__init__(name="放量上涨", description="成交量大于均量且价格上涨")
        self.volume_ratio = 2.0  # 成交量放大倍数

    async def analyze(self, data: pd.DataFrame) -> List[str]:
        """分析数据"""
        # 判断放量上涨
        volume_up = (data["volume"] > data["vma5"] * self.volume_ratio) & (
            data["close"] > data["close"].shift(1)
        )

        # 获取放量上涨股票
        signals = data[volume_up]
        return signals["code"].tolist()

    async def get_buy_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取买入信号"""
        df = await self.get_stock_data(code, date)
        if df.empty:
            return False

        # 判断是否放量上涨
        return (
            df["volume"].iloc[-1] > df["vma5"].iloc[-1] * self.volume_ratio
            and df["close"].iloc[-1] > df["close"].iloc[-2]
        )

    async def get_sell_signal(self, code: str, date: Optional[str] = None) -> bool:
        """获取卖出信号"""
        df = await self.get_stock_data(code, date)
        if df.empty:
            return False

        # 判断是否缩量下跌
        return (
            df["volume"].iloc[-1] < df["vma5"].iloc[-1]
            and df["close"].iloc[-1] < df["close"].iloc[-2]
        )
