"""Database CRUD operations for the Trading Order Management System.

This module provides Create, Read, Update, Delete (CRUD) operations for managing
trade orders in the database. It includes functions for retrieving, creating,
and updating orders using SQLAlchemy ORM.
"""

from sqlalchemy.orm import Session
from . import models, schemas
from typing import List

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    """Retrieve a list of orders from the database with pagination.

    Args:
        db (Session): The database session
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        List[models.Order]: A list of Order objects
    """
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    """Create a new order in the database.

    Args:
        db (Session): The database session
        order (schemas.OrderCreate): The order data to create

    Returns:
        models.Order: The created order object
    """
    db_order = models.Order(
        symbol=order.symbol,
        price=order.price,
        quantity=order.quantity,
        order_type=order.order_type
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> models.Order:
    """Retrieve a specific order by its ID.

    Args:
        db (Session): The database session
        order_id (int): The ID of the order to retrieve

    Returns:
        models.Order: The requested order object, or None if not found
    """
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order(db: Session, order_id: int, order: schemas.OrderCreate) -> models.Order:
    """Update an existing order in the database.

    Args:
        db (Session): The database session
        order_id (int): The ID of the order to update
        order (schemas.OrderCreate): The new order data

    Returns:
        models.Order: The updated order object, or None if not found
    """
    db_order = get_order(db, order_id)
    if db_order:
        # Update all fields from the input order
        for key, value in order.dict().items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order