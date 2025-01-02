import logging

from celery import shared_task

from app.core.database import get_celery_db
from app.stock.datastore import StockDatastore
from app.stock.depends import get_stock_indicator_service
from app.stock.service import StockService
from app.utils.date import SHORT_DATE_FORMAT, get_date, now_format

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def calculate_indicators_task(self, code: str, start_date: str = None):
    logger.info("start stock indicator task")
    if start_date is None:
        start_date = now_format(SHORT_DATE_FORMAT)
    with get_celery_db() as session:
        service = get_stock_indicator_service(session)
        service.calculate_indicators(code, get_date(start_date))
