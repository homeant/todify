from celery import chain, group
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.stock.data_service import StockDataService
from app.stock.datastore import StockDatastore
from app.utils.date import format_now
import logging
import asyncio

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def fetch_daily_data_task(self, date=None):
    """抓取日线数据的任务"""
    if not date:
        date = format_now("%Y%m%d")
    
    async def _fetch_daily():
        try:
            db = SessionLocal()
            stock_service = StockDataService(StockDatastore(db))
            await stock_service.fetch_daily_data(date)
            logger.info(f"完成抓取{date}日线数据")
        except Exception as e:
            logger.error(f"抓取日线数据失败: {str(e)}")
            raise e
        finally:
            db.close()
    
    try:
        asyncio.run(_fetch_daily())
    except Exception as e:
        raise self.retry(exc=e, countdown=60)  # 60秒后重试

@celery_app.task(bind=True, max_retries=3)
def fetch_lhb_data_task(self, date=None):
    """抓取龙虎榜数据的任务"""
    if not date:
        date = format_now("%Y%m%d")
    
    async def _fetch_lhb():
        try:
            db = SessionLocal()
            stock_service = StockDataService(StockDatastore(db))
            await stock_service.fetch_lhb_data(date)
            logger.info(f"完成抓取{date}龙虎榜数据")
        except Exception as e:
            logger.error(f"抓取龙虎榜数据失败: {str(e)}")
            raise e
        finally:
            db.close()
    
    try:
        asyncio.run(_fetch_lhb())
    except Exception as e:
        raise self.retry(exc=e, countdown=60)

@celery_app.task(bind=True, max_retries=3)
def fetch_block_trade_data_task(self, date=None):
    """抓取大宗交易数据的任务"""
    if not date:
        date = format_now("%Y%m%d")
    
    async def _fetch_block_trade():
        try:
            db = SessionLocal()
            stock_service = StockDataService(StockDatastore(db))
            await stock_service.fetch_block_trade_data(date)
            logger.info(f"完成抓取{date}大宗交易数据")
        except Exception as e:
            logger.error(f"抓取大宗交易数据失败: {str(e)}")
            raise e
        finally:
            db.close()
    
    try:
        asyncio.run(_fetch_block_trade())
    except Exception as e:
        raise self.retry(exc=e, countdown=60) 