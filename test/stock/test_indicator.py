from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.stock.datastore import StockDatastore
from app.stock.indicator_service import StockIndicatorService
from app.utils.date import date_parse_to_date


def test_indicator(session: Session):
    service = StockIndicatorService(StockDatastore(session))
    Base.metadata.create_all(engine)
    service.calculate_indicators("000001", date_parse_to_date("20241227"))
