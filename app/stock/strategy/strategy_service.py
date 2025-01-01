import logging
from datetime import date

from app.core.service import BaseService
from app.models.stock import StockSignal
from app.stock.datastore import StockDatastore
from app.stock.strategy.kdj_strategy import KDJStrategy
from app.stock.strategy.macd_strategy import MACDStrategy
from app.utils.date import date_parse
from app.utils.telegram import TelegramBot

logger = logging.getLogger(__name__)


class StrategyService(BaseService[StockDatastore, StockSignal]):
    """策略服务"""

    def __init__(self, datastore: StockDatastore):
        super().__init__(datastore)
        self.strategies = [
            MACDStrategy(),
            KDJStrategy(),
        ]
        self.telegram = TelegramBot()

    def generate_signals(self, code: str, start_date: date) -> None:
        """生成交易信号
        
        Args:
            code: 股票代码
            start_date: 开始保存信号的日期
        """
        try:
            # 获取开始日期前10天的指标数据用于计算
            calc_start_date = date_parse(start_date).shift(days=-10).date()
            indicators = self.datastore.get_indicator_history(code, calc_start_date)
            if not indicators:
                logger.warning(f"股票{code}没有指标数据")
                return

            # 运行每个策略
            for strategy in self.strategies:
                signals = strategy.generate_signals(indicators)
                # 只保留开始日期及之后的信号
                signals = [s for s in signals if s.trade_date >= start_date]
                self.datastore.bulk_save(signals, 10)



        except Exception as e:
            logger.exception(f"生成股票{code}的交易信号失败: {str(e)}")
