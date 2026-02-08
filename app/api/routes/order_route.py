from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, admin_required
from app.crud.order_crud import create_order, get_orders_for_user, get_all_orders, get_order_by_id
from app.schemas.order_schemas import OrderCreate, OrderOut
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order_route(order_data: OrderCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_order(db, order_data, user)


@router.get("/me", response_model=List[OrderOut])
async def get_my_orders(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_orders_for_user(db, user)


@router.get("/all", response_model=List[OrderOut])
async def get_all_orders_route(db: AsyncSession = Depends(get_db), user: User = Depends(admin_required)):
    return await get_all_orders(db)


@router.patch("/{order_id}/status")
async def update_order_status(order_id: int, new_status: str, db: AsyncSession = Depends(get_db), user: User = Depends(admin_required)):
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    from app.utils.enums import OrderStatusEnum
    try:
        order.status = OrderStatusEnum[new_status.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid status")

    await db.commit()
    await db.refresh(order)
    return {"status": "updated", "order_id": order.id, "new_status": order.status.name}
