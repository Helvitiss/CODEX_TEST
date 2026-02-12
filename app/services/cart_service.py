from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError
from app.repositories.cart_repository import CartRepository
from app.repositories.menu_repository import DishRepository


class CartService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.cart_repository = CartRepository(session)
        self.dish_repository = DishRepository(session)

    async def _get_or_create_active_cart(self, user_id: int | None, session_id: str | None):
        if user_id is None and not session_id:
            raise BadRequestError("session_id is required for guest cart")
        if user_id is not None:
            cart = await self.cart_repository.get_active_for_user(user_id)
        else:
            cart = await self.cart_repository.get_active_for_session(session_id or "")
        if cart is None:
            cart = await self.cart_repository.create(user_id=user_id, session_id=session_id)
            await self.session.flush()
        return cart

    async def add_item(self, user_id: int | None, session_id: str | None, dish_id: int, quantity: int):
        dish = await self.dish_repository.get(dish_id)
        if dish is None or not dish.is_available:
            raise BadRequestError("Dish unavailable")
        cart = await self._get_or_create_active_cart(user_id=user_id, session_id=session_id)
        existing_item = await self.cart_repository.get_item(cart_id=cart.id, dish_id=dish_id)
        if existing_item is not None:
            existing_item.quantity += quantity
        else:
            await self.cart_repository.create_item(
                cart_id=cart.id,
                dish_id=dish_id,
                quantity=quantity,
                unit_price=dish.price,
            )
        await self.session.commit()
        full_cart = await self.cart_repository.get_with_items(cart.id)
        return full_cart

    async def get_cart(self, user_id: int | None, session_id: str | None):
        if user_id is not None:
            cart = await self.cart_repository.get_active_for_user(user_id)
        else:
            if not session_id:
                raise BadRequestError("session_id is required for guest cart")
            cart = await self.cart_repository.get_active_for_session(session_id)
        if cart is None:
            cart = await self.cart_repository.create(user_id=user_id, session_id=session_id)
            await self.session.commit()
            return await self.cart_repository.get_with_items(cart.id)
        return cart
