from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.pizza_variant import PizzaVariant
from app.models.user import User

from app.schemas.order_schemas import OrderCreate  # если используешь pydantic

async def create_order(db: AsyncSession, order_data: OrderCreate, user: User | None) -> Order:
    total_price = 0
    items_db: list[OrderItem] = []

    for item in order_data.items:
        result = await db.execute(select(PizzaVariant).where(PizzaVariant.id == item.pizza_variant_id))
        variant = result.scalar_one_or_none()
        if not variant:
            raise ValueError(f"Pizza variant {item.pizza_variant_id} not found")

        price = variant.price
        total_price += price * item.quantity
        items_db.append(OrderItem(pizza_variant_id=variant.id, quantity=item.quantity, price=price))

    order = Order(
        user_id=user.id if user else None,
        customer_name=order_data.customer_name,
        customer_phone=order_data.customer_phone,
        total_price=total_price,
        items=items_db
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def get_orders_for_user(db: AsyncSession, user: User) -> List[Order]:
    result = await db.execute(select(Order).where(Order.user_id == user.id))
    return result.scalars().all()

async def get_all_orders(db: AsyncSession) -> List[Order]:
    result = await db.execute(select(Order))
    return result.scalars().all()

async def get_order_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()
