from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import OrderType

class OrderBase(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: OrderType

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True