from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.stock.datastore import StockDatastore
from app.stock.signal_service import StockSignalService
from app.utils.date import get_date


def test_signal(session: Session):
    service = StockSignalService(StockDatastore(session))
    Base.metadata.create_all(engine)
    service.calculate_signals("000001", get_date("20241202"))
