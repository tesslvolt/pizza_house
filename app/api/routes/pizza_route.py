from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.pizza_schemas import PizzaCreate, PizzaOut
from app.crud.pizza_crud import create_pizza, get_all_pizzas, get_pizza_by_id
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=PizzaOut)
async def api_create_pizza(pizza: PizzaCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_pizza(db, pizza)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PizzaOut])
async def api_get_all_pizzas(db: AsyncSession = Depends(get_db)):
    return await get_all_pizzas(db)

@router.get("/{pizza_id}", response_model=PizzaOut)
async def api_get_pizza(pizza_id: int, db: AsyncSession = Depends(get_db)):
    pizza = await get_pizza_by_id(db, pizza_id)
    if not pizza:
        raise HTTPException(status_code=404, detail="Пицца не найдена")
    return pizza
