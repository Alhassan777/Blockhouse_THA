"""Database models for the Trading Order Management System.

This module defines the SQLAlchemy ORM models used for storing and managing
trade orders in the database. It includes the Order model and related enums.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class OrderType(str, enum.Enum):
    """Enumeration for order types.

    Defines the possible types of trading orders in the system.
    Currently supports BUY and SELL orders.
    """
    BUY = "BUY"
    SELL = "SELL"

class Order(Base):
    """SQLAlchemy model for trade orders.

    This model represents a trade order in the system, storing information
    about the trade symbol, price, quantity, and type. It also includes
    timestamps for creation and updates.

    Attributes:
        id (int): Primary key for the order
        symbol (str): Trading symbol (e.g., 'AAPL', 'GOOGL')
        price (float): Price per unit of the order
        quantity (int): Number of units in the order
        order_type (OrderType): Type of order (BUY/SELL)
        created_at (datetime): Timestamp when the order was created
        updated_at (datetime): Timestamp when the order was last updated
    """
    __tablename__ = "orders"

    # Primary key and indexed columns
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    
    # Order details
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(Enum(OrderType))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        """Convert the order model to a dictionary.

        Returns:
            dict: Dictionary representation of the order
        """
        return {
            "id": self.id,
            "symbol": self.symbol,
            "price": self.price,
            "quantity": self.quantity,
            "order_type": self.order_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }