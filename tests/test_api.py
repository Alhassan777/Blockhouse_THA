import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
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

def test_create_order_invalid_data(client):
    # Test creating an order with invalid data
    invalid_order_data = {
        "symbol": "AAPL",
        "price": -100,  # Invalid negative price
        "quantity": 0,  # Invalid zero quantity
        "order_type": "INVALID"  # Invalid order type
    }
    response = client.post("/orders", json=invalid_order_data)
    assert response.status_code == 422

def test_create_order_missing_fields(client):
    # Test creating an order with missing required fields
    incomplete_order_data = {
        "symbol": "AAPL",
        "price": 150.50
        # Missing quantity and order_type
    }
    response = client.post("/orders", json=incomplete_order_data)
    assert response.status_code == 422

def test_create_order_special_symbols(client):
    # Test creating an order with special characters in symbol
    order_data = {
        "symbol": "BRK.A",  # Symbol with dot
        "price": 150.50,
        "quantity": 100,
        "order_type": "BUY"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    assert response.json()["symbol"] == "BRK.A"

def test_get_orders(client):
    # Test getting list of orders
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_orders_pagination(client):
    # Test orders pagination
    # Create multiple orders first
    for i in range(5):
        order_data = {
            "symbol": f"TEST{i}",
            "price": 100 + i,
            "quantity": 10 + i,
            "order_type": "BUY"
        }
        client.post("/orders", json=order_data)
    
    # Test pagination parameters
    response = client.get("/orders?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

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

def test_get_order_invalid_id(client):
    # Test getting an order with invalid ID format
    response = client.get("/orders/invalid_id")
    assert response.status_code == 422

def test_websocket_connection(client):
    # Test WebSocket connection and order notifications
    with client.websocket_connect("/ws") as websocket:
        # Create a new order to trigger WebSocket notification
        order_data = {
            "symbol": "TSLA",
            "price": 900.00,
            "quantity": 75,
            "order_type": "BUY"
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 200
        
        # Verify WebSocket receives the order notification
        data = websocket.receive_text()
        assert "New order created: TSLA" in data
        assert "BUY" in data
        assert "900.0" in data

def test_multiple_websocket_connections(client):
    # Test multiple WebSocket connections receiving notifications
    with client.websocket_connect("/ws") as websocket1, \
         client.websocket_connect("/ws") as websocket2:
        # Create a new order
        order_data = {
            "symbol": "MSFT",
            "price": 300.00,
            "quantity": 50,
            "order_type": "SELL"
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 200

        # Verify both WebSocket connections receive the notification
        data1 = websocket1.receive_text()
        data2 = websocket2.receive_text()
        assert data1 == data2
        assert "New order created: MSFT" in data1
        assert "SELL" in data1
        assert "300.0" in data1
