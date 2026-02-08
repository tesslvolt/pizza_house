from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from app.models.pizza_variant import PizzaVariant
from app.models.pizza import Pizza


async def get_all_pizzas(db: AsyncSession):
    result = await db.execute(
        select(Pizza).options(selectinload(Pizza.variants))
    )
    return result.scalars().all()


async def get_pizza_by_id(db: AsyncSession, pizza_id: int):
    result = await db.execute(
        select(Pizza)
        .options(selectinload(Pizza.variants))
        .where(Pizza.id == pizza_id)
    )
    return result.scalar_one_or_none()


async def create_pizza(
    db: AsyncSession,
    name: str,
    description: str | None = None,
    image_url: str | None = None
):
    pizza = Pizza(name=name, description=description, image_url=image_url)
    db.add(pizza)
    await db.commit()
    await db.refresh(pizza)

    await db.refresh(pizza, attribute_names=["variants"])
    return pizza


async def delete_pizza(db: AsyncSession, pizza_id: int):
    pizza = await get_pizza_by_id(db, pizza_id)
    if pizza:
        await db.delete(pizza)
        await db.commit()
    return pizza


async def create_variant(db: AsyncSession, pizza_id: int, size: str, price: float):
    variant = PizzaVariant(pizza_id=pizza_id, size=size, price=price)
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    return variant
