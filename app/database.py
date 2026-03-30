from sqlmodel import create_engine, SQLModel, Session, select, text
from typing import Generator

from app.config import DatabaseConfig

engine = create_engine(DatabaseConfig.uri, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def sql_connection_check() -> None:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            # Si no funciona intentar importar text de alchemy en lugar de model
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")
