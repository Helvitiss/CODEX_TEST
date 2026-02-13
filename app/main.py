from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routers.admin_dishes import router as admin_dishes_router
from app.api.routers.auth import router as auth_router
from app.api.routers.cart import router as cart_router
from app.api.routers.menu import router as menu_router
from app.api.routers.orders import router as orders_router
from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import AppError
from app.core.schema import ensure_dishes_image_path_column
from app.models import Base

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await ensure_dishes_image_path_column(connection)

    media_root = Path(settings.media_root)
    media_root.mkdir(parents=True, exist_ok=True)
    (media_root / settings.dish_media_subdir).mkdir(parents=True, exist_ok=True)

    media_root = Path(settings.media_root)
    media_root.mkdir(parents=True, exist_ok=True)
    (media_root / settings.dish_media_subdir).mkdir(parents=True, exist_ok=True)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(Exception)
async def unhandled_error_handler(_: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.mount("/media", StaticFiles(directory=str(settings.media_root)), name="media")

app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(admin_dishes_router)
