"""Pydantic schemas for the Trading Order Management System.

This module defines the Pydantic models used for request/response validation
and serialization in the API. It includes base schemas and their derivatives
for creating and retrieving orders.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import OrderType

class OrderBase(BaseModel):
    """Base Pydantic model for trade orders.

    This model serves as the base for all order-related schemas, defining
    the common fields that are required for both creating and retrieving orders.

    Attributes:
        symbol (str): The trading symbol (e.g., 'AAPL', 'GOOGL')
        price (float): The price per unit for the order
        quantity (int): The number of units in the order
        order_type (OrderType): The type of order (BUY/SELL)
    """
    symbol: str
    price: float
    quantity: int
    order_type: OrderType

class OrderCreate(OrderBase):
    """Pydantic model for creating new orders.

    Inherits all fields from OrderBase without adding any additional fields.
    Used for validating incoming order creation requests.
    """
    pass

class Order(OrderBase):
    """Pydantic model for complete order information.

    Extends the base order model with additional fields that are present
    in the database but not required for order creation.

    Attributes:
        id (int): The unique identifier for the order
        created_at (datetime): The timestamp when the order was created
        updated_at (Optional[datetime]): The timestamp when the order was last updated
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        """Pydantic model configuration.

        Enables ORM mode to allow the model to work with SQLAlchemy models.
        """
        orm_mode = True