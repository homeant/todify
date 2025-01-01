from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.stock.analysis_service import StockAnalysisService
from app.stock.datastore import StockDatastore
from app.stock.signal_service import StockSignalService
from app.utils.date import get_date


def test_analyze_signals(session: Session):
    service = StockAnalysisService(StockDatastore(session))
    Base.metadata.create_all(engine)
    service.analyze_signals("000001", get_date("20241231"))
