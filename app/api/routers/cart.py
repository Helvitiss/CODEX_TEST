from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.schemas.cart import CartAddItem, CartRead
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartRead)
async def get_cart(
    session_id: str | None = Header(default=None, alias="X-Session-ID"),
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    return await CartService(session).get_cart(user_id=user.id, session_id=session_id)


@router.get("/guest", response_model=CartRead)
async def get_guest_cart(
    session_id: str = Header(alias="X-Session-ID"),
    session: AsyncSession = Depends(get_db_session),
):
    return await CartService(session).get_cart(user_id=None, session_id=session_id)


@router.post("", response_model=CartRead)
async def add_to_cart(
    payload: CartAddItem,
    session_id: str | None = Header(default=None, alias="X-Session-ID"),
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    return await CartService(session).add_item(
        user_id=user.id,
        session_id=session_id,
        dish_id=payload.dish_id,
        quantity=payload.quantity,
    )


@router.post("/guest", response_model=CartRead)
async def add_to_guest_cart(
    payload: CartAddItem,
    session_id: str = Header(alias="X-Session-ID"),
    session: AsyncSession = Depends(get_db_session),
):
    return await CartService(session).add_item(
        user_id=None,
        session_id=session_id,
        dish_id=payload.dish_id,
        quantity=payload.quantity,
    )
