import logging
from typing import List

from app.models.stock import StockIndicator, StockSignal
from app.stock.signal._strategy import BaseStrategy

logger = logging.getLogger(__name__)


class KDJStrategy(BaseStrategy):
    """KDJ交叉策略"""

    name: str = "kdj_strategy"
    description: str = "KDJ金叉买入，死叉卖出"

    def generate_signals(
        self,
        indicators: List[StockIndicator],
    ) -> List[StockSignal]:
        signals = []

        if len(indicators) < 2:
            return signals

        sorted_indicators = sorted(indicators, key=lambda x: x.trade_date)

        for i in range(1, len(sorted_indicators)):
            prev, curr = sorted_indicators[i - 1], sorted_indicators[i]

            # 金叉：K线从下方穿过D线
            if prev.k < prev.d and curr.k > curr.d:
                signals.append(
                    StockSignal(
                        code=curr.code,
                        name=curr.name,
                        trade_date=curr.trade_date,
                        strategy=self.name,
                        signal_type="buy",
                        signal_desc=f"KDJ金叉: K从{prev.k:.2f}上升至{curr.k:.2f}, D从{prev.d:.2f}变为{curr.d:.2f}",
                    )
                )

            # 死叉：K线从上方穿过D线
            elif prev.k > prev.d and curr.k < curr.d:
                signals.append(
                    StockSignal(
                        code=curr.code,
                        name=curr.name,
                        trade_date=curr.trade_date,
                        strategy=self.name,
                        signal_type="sell",
                        signal_desc=f"KDJ死叉: K从{prev.k:.2f}下降至{curr.k:.2f}, D从{prev.d:.2f}变为{curr.d:.2f}",
                    )
                )

        return signals
