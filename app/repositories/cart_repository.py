from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart, CartItem


class CartRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_for_user(self, user_id: int) -> Cart | None:
        result = await self.session.execute(
            select(Cart)
            .where(Cart.user_id == user_id, Cart.is_active.is_(True))
            .options(selectinload(Cart.items))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_active_for_session(self, session_id: str) -> Cart | None:
        result = await self.session.execute(
            select(Cart)
            .where(Cart.session_id == session_id, Cart.is_active.is_(True))
            .options(selectinload(Cart.items))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int | None, session_id: str | None) -> Cart:
        cart = Cart(user_id=user_id, session_id=session_id, is_active=True)
        self.session.add(cart)
        await self.session.flush()
        return cart

    async def get_item(self, cart_id: int, dish_id: int) -> CartItem | None:
        result = await self.session.execute(
            select(CartItem).where(CartItem.cart_id == cart_id, CartItem.dish_id == dish_id)
        )
        return result.scalar_one_or_none()

    async def create_item(self, cart_id: int, dish_id: int, quantity: int, unit_price) -> CartItem:
        item = CartItem(cart_id=cart_id, dish_id=dish_id, quantity=quantity, unit_price=unit_price)
        self.session.add(item)
        await self.session.flush()
        return item

    async def get_with_items(self, cart_id: int) -> Cart | None:
        result = await self.session.execute(
            select(Cart).where(Cart.id == cart_id).options(selectinload(Cart.items))
        )
        return result.scalar_one_or_none()
