import logging

from celery import group, shared_task

from app.core.database import get_db
from app.stock.depends import get_stock_indicator_service, get_stock_service
from app.stock.trade_calendar import TradeCalendar
from app.utils.date import SHORT_DATE_FORMAT, date_format, date_parse, get_now

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def fetch_daily_data_task(self, start_date: str, end_date: str = None):
    """抓取日线数据的任务"""
    with get_db() as session:
        stock_service = get_stock_service(session)
        try:
            stock_service.fetch_daily_data(date_parse(start_date).date(), date_parse(end_date).date() if end_date else None)
            logger.info(f"完成抓取{start_date}日线数据")
        except Exception as ex:
            logger.exception(f"抓取日线数据失败: {str(ex)}")
            raise ex


@shared_task(bind=True, max_retries=3)
def fetch_lhb_data_task(self, start_date: str, end_date: str = None):
    """抓取龙虎榜数据的任务"""
    with get_db() as session:
        stock_service = get_stock_service(session)
        try:
            stock_service.fetch_lhb_data(date_parse(start_date).date(), date_parse(end_date).date() if end_date else None)
            logger.info(f"完成抓取{start_date}龙虎榜数据")
        except Exception as ex:
            logger.exception(f"抓取日线数据失败: {str(ex)}")
            raise ex


@shared_task(bind=True, max_retries=3)
def fetch_block_trade_data_task(self, start_date: str, end_date: str = None):
    """抓取大宗交易数据的任务"""
    with get_db() as session:
        stock_service = get_stock_service(session)
        stock_service.fetch_block_trade_data(date_parse(start_date).date(), date_parse(end_date).date() if end_date else None)
        logger.info(f"完成抓取{start_date}大宗交易数据")


@shared_task(bind=True, max_retries=3)
def fetch_daily_stock_data(self, start_date: str = None, end_date: str = None):
    if start_date:
        date = date_parse(start_date)
    else:
        date = get_now()
    date_str = date_format(date, SHORT_DATE_FORMAT)
    if TradeCalendar().is_trade_time(date):
        group(
            fetch_daily_data_task.s(),
            fetch_lhb_data_task.s(),
            fetch_block_trade_data_task.s(),
        ).apply(kwargs={"start_date": date_str, end_date: date_parse(end_date).date() if end_date else None})
        # stock_indicator_task.apply_async(kwargs={"date": date})
    else:
        logger.info(f"非交易日，不抓取数据, date: {date_str}")


@shared_task(bind=True, max_retries=3)
def stock_indicator_task(date: str):
    logger.exception("start stock indicator task")
    with get_db() as session:
        service = get_stock_indicator_service(session)
        service.calculate_indicators(date)
