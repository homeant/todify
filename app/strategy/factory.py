from typing import Dict, List, Type

from app.core.singleton import Singleton
from app.strategy.base import BaseStrategy
from app.strategy.boll_strategy import BollStrategy
from app.strategy.cci_strategy import CCIStrategy
from app.strategy.combo_strategy import ComboStrategy
from app.strategy.dmi_strategy import DMIStrategy
from app.strategy.kdj_cross import KDJStrategy
from app.strategy.macd_cross import MACDCrossStrategy
from app.strategy.rsi_strategy import RSIStrategy
from app.strategy.volume_up import VolumeUpStrategy


class StrategyFactory(metaclass=Singleton):
    """策略工厂"""

    def __init__(self):
        self._strategies: Dict[str, Type[BaseStrategy]] = {}
        self._register_strategies()

    def _register_strategies(self):
        """注册策略"""
        self._strategies = {
            "volume_up": VolumeUpStrategy,
            "macd_cross": MACDCrossStrategy,
            "kdj": KDJStrategy,
            "rsi": RSIStrategy,
            "boll": BollStrategy,
            "dmi": DMIStrategy,
            "cci": CCIStrategy,
            "combo": ComboStrategy,
        }

    def get_strategy(self, name: str) -> BaseStrategy:
        """获取策略实例"""
        strategy_class = self._strategies.get(name)
        if not strategy_class:
            raise ValueError(f"Strategy {name} not found")
        return strategy_class()

    def list_strategies(self) -> List[Dict]:
        """获取所有策略信息"""
        return [
            {"name": s().name, "description": s().description}
            for s in self._strategies.values()
        ]
