from sqlalchemy.orm import Session

from app.stock.depends import get_stock_service
from app.stock.trade_calendar import TradeCalendar
from app.utils.date import date_parse


def test_hot_rank(db_session: Session):
    TradeCalendar().is_trade_time()
    service = get_stock_service(db_session)

    service.fetch_daily_data(date_parse('20240701').date(), None)
