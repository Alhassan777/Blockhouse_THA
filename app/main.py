"""FastAPI Trading Order Management System

This module implements a RESTful API service for managing trading orders with real-time
WebSocket notifications. It provides endpoints for creating, reading, and updating trade
orders, along with WebSocket support for real-time order updates.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trade Orders API",
    description="A REST API for handling trade orders with real-time updates",
    version="1.0.0"
)

# Configure CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows cookies in cross-origin requests
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ConnectionManager:
    """Manages WebSocket connections for real-time order updates.

    This class handles the lifecycle of WebSocket connections, including
    connection establishment, disconnection, and broadcasting messages
    to all connected clients.
    """

    def __init__(self):
        """Initialize the connection manager with an empty list of connections."""
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection and add it to active connections.

        Args:
            websocket (WebSocket): The WebSocket connection to be added
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from active connections.

        Args:
            websocket (WebSocket): The WebSocket connection to be removed
        """
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Broadcast a message to all connected clients.

        Args:
            message (str): The message to be broadcast to all connections
        """
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message.

    Returns:
        dict: A welcome message for the API
    """
    return {"message": "Welcome to Trade Orders API"}

@app.post("/orders", response_model=schemas.Order)
async def create_trade_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Create a new trade order and broadcast a notification.

    Args:
        order (schemas.OrderCreate): The order data to create
        db (Session): The database session

    Returns:
        models.Order: The created order
    """
    db_order = crud.create_order(db=db, order=order)
    await manager.broadcast(f"New order created: {order.symbol} - {order.order_type} - {order.quantity} @ {order.price}")
    return db_order

@app.get("/orders", response_model=List[schemas.Order])
def get_trade_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of trade orders with pagination.

    Args:
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        db (Session): The database session

    Returns:
        List[models.Order]: List of orders
    """
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_trade_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific trade order by ID.

    Args:
        order_id (int): The ID of the order to retrieve
        db (Session): The database session

    Returns:
        models.Order: The requested order

    Raises:
        HTTPException: If the order is not found
    """
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time order updates.

    Handles WebSocket connections for real-time order notifications.
    Clients can connect to this endpoint to receive order updates.

    Args:
        websocket (WebSocket): The WebSocket connection
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Order update: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)