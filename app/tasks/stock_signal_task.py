import logging

import akshare as ak
from celery import shared_task

from app.core.database import get_celery_db
from app.stock.datastore import StockDatastore
from app.stock.signal_service import StockSignalService
from app.utils.date import SHORT_DATE_FORMAT, get_date, now_format

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def calculate_signals_task(self, start_date: str = None):
    logger.info("start stock indicator task")
    if start_date is None:
        start_date = now_format(SHORT_DATE_FORMAT)
    with get_celery_db() as session:
        stock_info = ak.stock_info_a_code_name()
        service = StockSignalService(StockDatastore(session))
        for _, row in stock_info.iterrows():
            service.calculate_signals(row["code"], get_date(start_date))
