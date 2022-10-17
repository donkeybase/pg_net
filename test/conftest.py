import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


@pytest.fixture(scope="function")
def engine():
    engine = create_engine("postgresql:///postgres")
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def sess(engine):

    session = Session(engine)

    # Reset sequences and tables between tests
    session.execute(
        """
    create extension if not exists pg_net;
    """
    )
    session.commit()

    yield session

    session.rollback()

    session.execute(
        """
    drop extension pg_net cascade;
    create extension if not exists pg_net;
    """
    )
    session.commit()
