from pydantic import BaseModel
from typing import List
from app.common.enums import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    status: OrderStatus
    total_amount: float
    items: List[OrderItemOut]
    class Config:
        from_attributes = True


