import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.models import Order

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test database engine
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    # Create test database tables
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        # Drop test database tables after tests
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    # Create a test client using the FastAPI app
    return TestClient(app)

def test_read_main(client):
    # Test the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Trade Orders API"}

def test_create_order(client):
    # Test creating a new order
    order_data = {
        "symbol": "AAPL",
        "price": 150.50,
        "quantity": 100,
        "order_type": "BUY"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == order_data["symbol"]
    assert data["price"] == order_data["price"]
    assert data["quantity"] == order_data["quantity"]
    assert data["order_type"] == order_data["order_type"]
    assert "id" in data

def test_get_orders(client):
    # Test getting list of orders
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_order(client):
    # Test getting a specific order
    # First create an order
    order_data = {
        "symbol": "GOOGL",
        "price": 2500.75,
        "quantity": 50,
        "order_type": "SELL"
    }
    create_response = client.post("/orders", json=order_data)
    order_id = create_response.json()["id"]

    # Then retrieve it
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == order_data["symbol"]
    assert data["price"] == order_data["price"]

def test_get_nonexistent_order(client):
    # Test getting a non-existent order
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

def test_websocket_connection(client):
    # Test WebSocket connection
    with client.websocket_connect("/ws") as websocket:
        # Test sending and receiving a message
        websocket.send_text("Test message")
        data = websocket.receive_text()
        assert "Order update: Test message" in data