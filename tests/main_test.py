from fastapi.testclient import TestClient
from app.main import app, get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, StaticPool
from app.models import Base, TicketModel
from app.schemas import Status
from datetime import datetime, timezone
import pytest

db_url = "sqlite:///:memory:"
engine = create_engine(db_url, connect_args={'check_same_thread': False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    fixed_date = datetime(2024, 12, 31, 12, 0, 0, tzinfo=timezone.utc)
    db_ticket = TicketModel(number=123, date=fixed_date, status=Status.WAITING)
    session.add(db_ticket)
    session.commit()
    session.close()
    yield
    Base.metadata.drop_all(bind=engine)

def test_check_server_hi(setup_db):
    response = client.get("/")
    assert response.status_code == 200
    result = response.json()
    expected = {"message": "Server is running"}
    assert result == expected

def test_tickets_len(setup_db):
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_tickets_content(setup_db):
    response = client.get("/tickets/")
    assert response.status_code == 200
    result = response.json()
    expected = [{"id": 1, "number": 123, "date": "2024-12-31T12:00:00", "status": Status.WAITING.value}]
    assert result == expected

def test_create_ticket(setup_db):
    response = client.post("/create_ticket/")
    assert response.status_code == 200
    result = response.json()
    assert result["number"] == 124
    assert result["status"] == Status.WAITING.value

def test_process_next_ticket(setup_db):
    response = client.put("/next_ticket/")
    assert response.status_code == 200
    result = response.json()
    expected = {"id": 1, "number": 123, "date": "2024-12-31T12:00:00", "status": Status.PROCESSED.value}
    assert result == expected