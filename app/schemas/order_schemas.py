from pydantic import BaseModel
from typing import List
from enum import Enum


class OrderStatusEnum(str, Enum):
    CREATED = "created"
    COMPLETED = "completed"
    CANCELED = "canceled"


class OrderItemBase(BaseModel):
    pizza_variant_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    price: float

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderOut(OrderBase):
    id: int
    user_id: int | None = None
    status: OrderStatusEnum
    total_price: float
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
