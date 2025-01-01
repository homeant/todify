import logging
from datetime import date

from app.core.service import BaseService
from app.models.stock import StockSignal
from app.stock.datastore import StockDatastore
from app.utils.date import get_date, get_today

logger = logging.getLogger(__name__)


class StockSignalService(BaseService[StockDatastore, StockSignal]):
    """股票信号计算服务"""

    def __init__(self, datastore: StockDatastore):
        super().__init__(datastore)

    def calculate_signals(self, code: str, start_date: date):
        """计算指定日期开始的技术信号

        Args:
            code: 股票代码
            start_date: 开始日期
        """
        try:
            current_date = start_date
            today = get_today()

            while current_date <= today:
                # 获取当日指标数据
                current_indicator = self.datastore.get_indicator(code, current_date)
                if not current_indicator:
                    current_date = get_date(current_date, days=1)
                    continue

                # 获取当日股票数据
                stock_daily = self.datastore.get_stock_daily(code, current_date)
                if not stock_daily:
                    current_date = get_date(current_date, days=1)
                    continue

                # 获取前一天的指标数据
                prev_indicator = self.datastore.get_indicator(code, get_date(current_date, days=-1))
                if not prev_indicator:
                    current_date = get_date(current_date, days=1)
                    continue

                stock_name = current_indicator.name
                if not stock_name:
                    stock_name = stock_daily.name

                # 计算所有信号
                signal = StockSignal(
                    code=code,
                    name=stock_name,
                    trade_date=current_date,
                    # MACD信号
                    macd_golden_cross=prev_indicator.diff < prev_indicator.dea and current_indicator.diff > current_indicator.dea,
                    macd_dead_cross=prev_indicator.diff > prev_indicator.dea and current_indicator.diff < current_indicator.dea,
                    # KDJ信号
                    kdj_golden_cross=prev_indicator.k < prev_indicator.d and current_indicator.k > current_indicator.d,
                    kdj_dead_cross=prev_indicator.k > prev_indicator.d and current_indicator.k < current_indicator.d,
                    kdj_oversold=current_indicator.k < 20,
                    kdj_overbought=current_indicator.k > 80,
                    # RSI信号
                    rsi_oversold=current_indicator.rsi6 < 20,
                    rsi_overbought=current_indicator.rsi6 > 80,
                    # 布林带信号
                    boll_break_up=stock_daily.close > current_indicator.boll_up,
                    boll_break_down=stock_daily.close < current_indicator.boll_down,
                    # 均线信号
                    ma_golden_cross=prev_indicator.ma5 < prev_indicator.ma20 and current_indicator.ma5 > current_indicator.ma20,
                    ma_dead_cross=prev_indicator.ma5 > prev_indicator.ma20 and current_indicator.ma5 < current_indicator.ma20,
                )

                # 检查是否有任何信号为True
                has_signal = any(
                    [
                        signal.macd_golden_cross,
                        signal.macd_dead_cross,
                        signal.kdj_golden_cross,
                        signal.kdj_dead_cross,
                        signal.kdj_oversold,
                        signal.kdj_overbought,
                        signal.rsi_oversold,
                        signal.rsi_overbought,
                        signal.boll_break_up,
                        signal.boll_break_down,
                        signal.ma_golden_cross,
                        signal.ma_dead_cross,
                    ]
                )

                # 只有在有信号时才保存
                if has_signal:
                    self.datastore.upsert(signal)
                    logger.info(
                        f"发现股票{code}在{current_date}的信号，已保存\n"
                        f"MACD金叉:{signal.macd_golden_cross} 死叉:{signal.macd_dead_cross}\n"
                        f"KDJ金叉:{signal.kdj_golden_cross} 死叉:{signal.kdj_dead_cross} "
                        f"超卖:{signal.kdj_oversold} 超买:{signal.kdj_overbought}\n"
                        f"RSI超卖:{signal.rsi_oversold} 超买:{signal.rsi_overbought}\n"
                        f"布林带上穿:{signal.boll_break_up} 下穿:{signal.boll_break_down}\n"
                        f"MA金叉:{signal.ma_golden_cross} 死叉:{signal.ma_dead_cross}"
                    )
                else:
                    logger.info(f"股票{code}在{current_date}没有发现任何信号")

                # 移动到下一天
                current_date = get_date(current_date, days=1)

        except Exception as e:
            logger.exception(f"计算股票{code}的信号时发生错误: {str(e)}")
            raise e
