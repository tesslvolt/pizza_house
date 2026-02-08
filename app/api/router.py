from fastapi import APIRouter
from app.api.routes import auth_route, order_route, pizza_route

api_router = APIRouter()

api_router.include_router(auth_route.router)
api_router.include_router(order_route.router, prefix="/orders", tags=["orders"])
api_router.include_router(pizza_route.router, prefix="/pizzas", tags=["pizzas"])
