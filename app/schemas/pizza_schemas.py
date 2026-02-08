from pydantic import BaseModel
from typing import List, Optional

class PizzaVariantBase(BaseModel):
    size: str
    price: float

class PizzaVariantCreate(PizzaVariantBase):
    pizza_id: int

class PizzaVariantOut(PizzaVariantBase):
    id: int
    pizza_id: int

    class Config:
        orm_mode = True

class PizzaBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    image_url: Optional[str] = None

class PizzaCreate(PizzaBase):
    pass

class PizzaOut(PizzaBase):
    id: int
    variants: List[PizzaVariantOut] = []

    class Config:
        from_attributes = True
