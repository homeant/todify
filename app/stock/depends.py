from sqlalchemy.orm import Session

from app.stock.datastore import StockDatastore
from app.stock.service import StockService


def det_stock_datastore(db_session: Session) -> StockDatastore:
    return StockDatastore(db_session)

def get_stock_service(
    db_session: Session
) -> StockService:
    return StockService(
        datastore=det_stock_datastore(db_session)
    )
