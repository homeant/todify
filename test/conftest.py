import pytest
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import engine


@pytest.fixture(scope='function')
def session():
    """Creates a new database session for a test."""
    SessionLocal = sessionmaker(engine)
    session = SessionLocal()

    yield session

    session.close()
    engine.dispose()


@pytest.fixture(name="db_session")
def db_session_fixture() -> Session:
    session = sessionmaker(bind=engine, expire_on_commit=False)
    with session() as session:
        yield session
    engine.dispose()