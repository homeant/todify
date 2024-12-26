import asyncio
import logging

from celery import shared_task

from app.core.database import get_db
from app.main import celery_app
from app.stock.depends import get_stock_service
from app.utils.date import format_now, SHORT_DATE_FORMAT

logger = logging.getLogger(__name__)

@shared_task()
def fetch_daily_data_task():
    """抓取日线数据的任务"""
    date = format_now(SHORT_DATE_FORMAT)
    with get_db() as session:
        stock_service = get_stock_service(session)
        try:
            stock_service.fetch_daily_data(date)
            logger.info(f"完成抓取{date}日线数据")
        except Exception as ex:
            logger.exception(f"抓取日线数据失败: {str(ex)}")
            raise ex

@shared_task()
def fetch_lhb_data_task():
    """抓取龙虎榜数据的任务"""
    date = format_now(SHORT_DATE_FORMAT)
    with get_db() as session:
        stock_service = get_stock_service(session)
        try:
            stock_service.fetch_lhb_data(date)
            logger.info(f"完成抓取{date}龙虎榜数据")
        except Exception as ex:
            logger.exception(f"抓取日线数据失败: {str(ex)}")
            raise ex

@shared_task()
def fetch_block_trade_data_task():
    """抓取大宗交易数据的任务"""
    date = format_now(SHORT_DATE_FORMAT)
    with get_db() as session:
        stock_service = get_stock_service(session)
        stock_service.fetch_block_trade_data(date)
        logger.info(f"完成抓取{date}大宗交易数据")