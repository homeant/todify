import logging

from app.core.database import SessionLocal
from app.stock.data_service import StockDataService
from app.stock.datastore import StockDatastore
from app.stock.indicator_service import IndicatorService
from app.stock.signal_service import SignalService
from app.utils.date import format_now

logger = logging.getLogger(__name__)


async def run_stock_daily_job():
    """执行每日数据抓取任务"""
    try:
        date = format_now("%Y%m%d")

        # 创建服务
        db = SessionLocal()
        stock_service = StockDataService(StockDatastore(db))
        indicator_service = IndicatorService(StockDatastore(db))
        signal_service = SignalService(StockDatastore(db))

        # 抓取数据
        logger.info(f"开始抓取{date}数据...")

        # 抓取日线数据
        await stock_service.fetch_daily_data(date)
        logger.info(f"完成抓取{date}日线数据")

        # 抓取龙虎榜数据
        await stock_service.fetch_lhb_data(date)
        logger.info(f"完成抓取{date}龙虎榜数据")

        # 抓取大宗交易数据
        await stock_service.fetch_block_trade_data(date)
        logger.info(f"完成抓取{date}大宗交易数据")

        # 计算技术指标
        stocks = await stock_service.get_all_stocks()
        for stock in stocks:
            await indicator_service.calculate_indicators(stock.code, date)
        logger.info(f"完成计算{date}技术指标")

        # 生成交易信号
        await signal_service.generate_signals(date)
        logger.info(f"完成生成{date}交易信号")

    except Exception as e:
        logger.error(f"抓取数据失败:{str(e)}")
    finally:
        db.close()
