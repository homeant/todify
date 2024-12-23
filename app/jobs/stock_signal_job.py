import logging
from app.core.database import SessionLocal
from app.stock.datastore import StockDatastore
from app.stock.signal_service import SignalService
from app.utils.date import format_now

logger = logging.getLogger(__name__)

async def run_stock_signal_job():
    """执行交易信号生成任务"""
    try:
        date = format_now("%Y%m%d")
        
        # 创建服务
        db = SessionLocal()
        signal_service = SignalService(StockDatastore(db))
        
        # 生成信号
        logger.info(f"开始生成{date}交易信号...")
        await signal_service.generate_signals(date)
        logger.info(f"完成生成{date}交易信号")
        
    except Exception as e:
        logger.error(f"生成交易信号失败:{str(e)}")
    finally:
        db.close() 