import logging
from datetime import date

from sqlalchemy.orm import Session

from app.stock.depends import get_stock_service
from app.stock.trade_calendar import TradeCalendar
from app.utils.date import date_parse

logger = logging.getLogger(__name__)


def test_fetch_stock_infos(db_session: Session):
    service = get_stock_service(db_session)
    service.fetch_daily_data(start_date=date_parse("20250103").date())


def test_fetch_lhb_data(db_session: Session):
    TradeCalendar().is_trade_day()
    service = get_stock_service(db_session)

    service.fetch_lhb_data(date_parse("20240701").date(), date.today())


def test_fetch_block_trade_data(db_session: Session):
    TradeCalendar().is_trade_day()
    service = get_stock_service(db_session)

    service.fetch_block_trade_data(date_parse("20240701").date(), date.today())
