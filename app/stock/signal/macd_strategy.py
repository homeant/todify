import logging
from typing import List

from app.models.stock import StockIndicator, StockSignal
from app.stock.signal._strategy import BaseStrategy

logger = logging.getLogger(__name__)


class MACDStrategy(BaseStrategy):
    """MACD金叉死叉策略"""

    name: str = "macd_strategy"
    description: str = "MACD金叉买入，死叉卖出"

    def generate_signals(
        self,
        indicators: List[StockIndicator],
    ) -> List[StockSignal]:
        signals = []

        # 至少需要两天数据才能判断交叉
        if len(indicators) < 2:
            return signals

        # 按日期排序
        sorted_indicators = sorted(indicators, key=lambda x: x.trade_date)

        for i in range(1, len(sorted_indicators)):
            prev, curr = sorted_indicators[i - 1], sorted_indicators[i]

            # 金叉：DIFF从下方穿过DEA
            if prev.diff < prev.dea and curr.diff > curr.dea:
                signals.append(
                    StockSignal(
                        code=curr.code,
                        name=curr.name,
                        trade_date=curr.trade_date,
                        strategy=self.name,
                        signal_type="buy",
                        signal_desc=f"MACD金叉: DIFF从{prev.diff:.2f}上升至{curr.diff:.2f}, DEA从{prev.dea:.2f}变为{curr.dea:.2f}",
                    )
                )

            # 死叉：DIFF从上方穿过DEA
            elif prev.diff > prev.dea and curr.diff < curr.dea:
                signals.append(
                    StockSignal(
                        code=curr.code,
                        name=curr.name,
                        trade_date=curr.trade_date,
                        strategy=self.name,
                        signal_type="sell",
                        signal_desc=f"MACD死叉: DIFF从{prev.diff:.2f}下降至{curr.diff:.2f}, DEA从{prev.dea:.2f}变为{curr.dea:.2f}",
                    )
                )

        return signals
