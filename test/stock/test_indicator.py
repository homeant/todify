from sqlalchemy.orm import Session

from app.stock.datastore import StockDatastore
from app.stock.indicator_service import StockIndicatorService


def test_indicator(session: Session):
    service = StockIndicatorService(StockDatastore(session))
    service.calculate_indicators("603890", '20241227')

