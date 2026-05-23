# tests/conftest.py
import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session
from fastapi.testclient import TestClient

# 1. Creamos un engine de SQLite en memoria exclusivo para los tests
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


# 2. Creamos una "fixture" que prepare las tablas antes de cada test y las borre al terminar
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)  # Crea las tablas limpias
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)  # Borra todo al terminar el test


# 3. Creamos el cliente HTTP de pruebas inyectando la sesión temporal
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    # Sobreescribimos la dependencia original de FastAPI por la de test
    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    # Al terminar las pruebas, limpiamos la sobreescritura
    app.dependency_overrides.clear()
