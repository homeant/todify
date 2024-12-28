import logging

from celery import shared_task, group

from app.core.database import get_db
from app.stock.depends import get_stock_service
from app.stock.trade_calendar import TradeCalendar
from app.utils.date import SHORT_DATE_FORMAT, get_now, date_format

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def fetch_daily_data_task(self, date: str):
    """抓取日线数据的任务"""
    with get_db() as session:
        stock_service = get_stock_service(session)
        try:
            stock_service.fetch_daily_data(date)
            logger.info(f"完成抓取{date}日线数据")
        except Exception as ex:
            logger.exception(f"抓取日线数据失败: {str(ex)}")
            raise ex

@shared_task(bind=True, max_retries=3)
def fetch_lhb_data_task(self, date: str):
    """抓取龙虎榜数据的任务"""
    with get_db() as session:
        stock_service = get_stock_service(session)
        try:
            stock_service.fetch_lhb_data(date)
            logger.info(f"完成抓取{date}龙虎榜数据")
        except Exception as ex:
            logger.exception(f"抓取日线数据失败: {str(ex)}")
            raise ex

@shared_task(bind=True, max_retries=3)
def fetch_block_trade_data_task(self, date: str):
    """抓取大宗交易数据的任务"""
    with get_db() as session:
        stock_service = get_stock_service(session)
        stock_service.fetch_block_trade_data(date)
        logger.info(f"完成抓取{date}大宗交易数据")


@shared_task(bind=True, max_retries=3)
def fetch_daily_stock_data(self):
    now = get_now()
    if TradeCalendar().is_trade_time(now):
        date = date_format(now, SHORT_DATE_FORMAT)
        group(
            fetch_daily_data_task.s(),
            fetch_lhb_data_task.s(),
            fetch_block_trade_data_task.s()
        ).apply_async(
            kwargs={"date": date},
        )
    else:
        logger.info(f"非交易日，不抓取数据")