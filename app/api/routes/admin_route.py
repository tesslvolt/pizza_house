from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
import os

from app.core.database import get_db
from app.api.deps import admin_required
from app.crud.pizza_crud import (
    get_all_pizzas,
    create_pizza,
    delete_pizza,
    create_variant,
)
from app.models import User
from app.schemas.pizza_schemas import (
    PizzaVariantCreate,
    PizzaOut,
    PizzaVariantOut,
)
from app.crud.order_crud import get_all_orders

router = APIRouter(tags=["Admin"])


@router.get("/orders")
async def get_orders(
    current_admin: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_orders(db)


@router.get("/pizzas", response_model=List[PizzaOut])
async def get_pizzas(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_required),
):
    return await get_all_pizzas(db)


@router.post("/pizzas", response_model=PizzaOut)
async def create_pizza_route(
    name: str = Form(...),
    description: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_required),
):
    image_url = None

    if image:
        upload_dir = "app/static/images/pizzas"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = f"/static/images/pizzas/{image.filename}"

    pizza = await create_pizza(
        db=db,
        name=name,
        description=description,
        image_url=image_url,
    )

    return pizza


@router.delete("/pizzas/{pizza_id}", response_model=PizzaOut)
async def delete_pizza_route(
    pizza_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_required),
):
    pizza = await delete_pizza(db, pizza_id)
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    return pizza


@router.post("/pizza-variants", response_model=PizzaVariantOut)
async def create_pizza_variant_route(
    variant: PizzaVariantCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(admin_required),
):
    return await create_variant(
        db=db,
        pizza_id=variant.pizza_id,
        size=variant.size,
        price=variant.price,
    )
