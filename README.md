# Trading Order Management System

A FastAPI-based RESTful API service for managing trading orders with real-time WebSocket notifications.

## Features

- Create, read, and update trading orders
- Real-time order notifications via WebSocket
- SQLAlchemy ORM with SQLite database (configurable)
- FastAPI with automatic API documentation
- Docker support
- GitHub Actions for CI/CD

## Project Structure

```
.
├── .github/workflows/    # GitHub Actions workflows
├── app/                  # Application source code
│   ├── crud.py          # Database CRUD operations
│   ├── database.py      # Database configuration
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # SQLAlchemy models
│   └── schemas.py       # Pydantic schemas
├── Dockerfile           # Docker configuration
└── requirements.txt     # Python dependencies
```

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables (optional):
```bash
export DATABASE_URL="sqlite:///./orders.db"  # Default SQLite database
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t trading-orders .
```

2. Run the container:
```bash
docker run -p 8000:8000 trading-orders
```

## API Endpoints

### REST API

- `GET /orders` - List all orders
- `POST /orders` - Create a new order
- `GET /orders/{order_id}` - Get a specific order
- `PUT /orders/{order_id}` - Update an order

### WebSocket

- `WS /ws` - WebSocket endpoint for real-time order notifications

## Data Models

### Order

```python
{
    "id": int,
    "symbol": str,
    "price": float,
    "quantity": int,
    "order_type": str ("BUY" or "SELL"),
    "created_at": datetime,
    "updated_at": datetime
}
```

