from datetime import date

from sqlalchemy.orm import Session

from app.stock.depends import get_stock_service
from app.stock.trade_calendar import TradeCalendar
from app.utils.date import date_parse


def test_fetch_daily_data(db_session: Session):
    TradeCalendar().is_trade_day()
    service = get_stock_service(db_session)

    service.fetch_daily_data(date_parse("20240701").date(), date.today())


def test_fetch_lhb_data(db_session: Session):
    TradeCalendar().is_trade_day()
    service = get_stock_service(db_session)

    service.fetch_lhb_data(date_parse("20240701").date(), date.today())


def test_fetch_block_trade_data(db_session: Session):
    TradeCalendar().is_trade_day()
    service = get_stock_service(db_session)

    service.fetch_block_trade_data(date_parse("20240701").date(), date.today())
