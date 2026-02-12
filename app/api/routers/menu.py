from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_admin
from app.dependencies.common import pagination_params
from app.schemas.common import MessageResponse
from app.schemas.menu import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    DishCreate,
    DishRead,
    DishUpdate,
)
from app.services.menu_service import MenuService

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/categories", response_model=list[CategoryRead])
async def list_categories(
    pagination: tuple[int, int] = Depends(pagination_params),
    session: AsyncSession = Depends(get_db_session),
):
    limit, offset = pagination
    service = MenuService(session)
    return await service.list_categories(limit=limit, offset=offset)


@router.post("/categories", response_model=CategoryRead, dependencies=[Depends(get_current_admin)])
async def create_category(payload: CategoryCreate, session: AsyncSession = Depends(get_db_session)):
    return await MenuService(session).create_category(payload)


@router.put("/categories/{category_id}", response_model=CategoryRead, dependencies=[Depends(get_current_admin)])
async def update_category(category_id: int, payload: CategoryUpdate, session: AsyncSession = Depends(get_db_session)):
    return await MenuService(session).update_category(category_id, payload)


@router.delete(
    "/categories/{category_id}",
    response_model=MessageResponse,
    dependencies=[Depends(get_current_admin)],
    status_code=status.HTTP_200_OK,
)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_db_session)):
    await MenuService(session).delete_category(category_id)
    return MessageResponse(message="Category deleted")


@router.get("/dishes", response_model=list[DishRead])
async def list_dishes(
    pagination: tuple[int, int] = Depends(pagination_params),
    category_id: int | None = Query(default=None),
    is_available: bool | None = Query(default=None),
    session: AsyncSession = Depends(get_db_session),
):
    limit, offset = pagination
    return await MenuService(session).list_dishes(limit, offset, category_id, is_available)


@router.post("/dishes", response_model=DishRead, dependencies=[Depends(get_current_admin)])
async def create_dish(payload: DishCreate, session: AsyncSession = Depends(get_db_session)):
    return await MenuService(session).create_dish(payload)


@router.put("/dishes/{dish_id}", response_model=DishRead, dependencies=[Depends(get_current_admin)])
async def update_dish(dish_id: int, payload: DishUpdate, session: AsyncSession = Depends(get_db_session)):
    return await MenuService(session).update_dish(dish_id, payload)


@router.delete("/dishes/{dish_id}", response_model=MessageResponse, dependencies=[Depends(get_current_admin)])
async def delete_dish(dish_id: int, session: AsyncSession = Depends(get_db_session)):
    await MenuService(session).delete_dish(dish_id)
    return MessageResponse(message="Dish deleted")
