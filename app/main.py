from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse

from app.api.routes import (
    auth_route,
    pizza_route,
    order_route,
    admin_route,
)

app = FastAPI(
    title="Pizza House🍕 ",
)

BASE_DIR = Path(__file__).resolve().parent.parent

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(BASE_DIR / "static" / "index.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(
    auth_route.router,
    prefix="/api/auth",
    tags=["Auth"],
)

app.include_router(
    pizza_route.router,
    prefix="/api/pizzas",
    tags=["Pizzas"],
)

app.include_router(
    order_route.router,
    prefix="/api/orders",
    tags=["Orders"],
)

app.include_router(
    admin_route.router,
    prefix="/api/admin",
    tags=["Admin"],
)

