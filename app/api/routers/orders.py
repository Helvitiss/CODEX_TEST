from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_admin, get_current_user
from app.dependencies.common import pagination_params
from app.models.enums import OrderStatus
from app.schemas.order import CreateOrderRequest, OrderRead, UpdateOrderStatusRequest
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderRead)
async def create_order(
    payload: CreateOrderRequest,
    session_id: str | None = Header(default=None, alias="X-Session-ID"),
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    return await OrderService(session).create_from_cart(user.id, session_id, payload.phone_number)


@router.post("/guest", response_model=OrderRead)
async def create_guest_order(
    payload: CreateOrderRequest,
    session_id: str = Header(alias="X-Session-ID"),
    session: AsyncSession = Depends(get_db_session),
):
    return await OrderService(session).create_from_cart(None, session_id, payload.phone_number)


@router.get("/my", response_model=list[OrderRead])
async def my_orders(
    pagination: tuple[int, int] = Depends(pagination_params),
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    limit, offset = pagination
    return await OrderService(session).list_my_orders(user.id, limit, offset)


@router.get("", response_model=list[OrderRead], dependencies=[Depends(get_current_admin)])
async def all_orders(
    pagination: tuple[int, int] = Depends(pagination_params),
    status: OrderStatus | None = Query(default=None),
    session: AsyncSession = Depends(get_db_session),
):
    limit, offset = pagination
    return await OrderService(session).list_all_orders(limit=limit, offset=offset, status=status)


@router.patch("/{order_id}/status", response_model=OrderRead, dependencies=[Depends(get_current_admin)])
async def update_order_status(
    order_id: int,
    payload: UpdateOrderStatusRequest,
    session: AsyncSession = Depends(get_db_session),
):
    return await OrderService(session).update_order_status(order_id=order_id, status=payload.status)
