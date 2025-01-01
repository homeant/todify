from typing import List

from app.models.stock import StockIndicator, StockSignal


class BaseStrategy:
    """策略基类"""

    name: str = "base_strategy"
    description: str = "基础策略"

    def generate_signals(
        self,
        indicators: List[StockIndicator],
    ) -> List[StockSignal]:
        """生成交易信号"""
        raise NotImplementedError
