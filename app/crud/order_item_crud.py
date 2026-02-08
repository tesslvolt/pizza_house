from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.order_item import OrderItem

async def get_order_item_by_id(db: AsyncSession, item_id: int) -> Optional[OrderItem]:
    result = await db.execute(select(OrderItem).where(OrderItem.id == item_id))
    return result.scalar_one_or_none()

async def delete_order_item(db: AsyncSession, item: OrderItem):
    await db.delete(item)
    await db.commit()
