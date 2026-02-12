from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, NotFoundError
from app.models.enums import OrderStatus
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository
from app.services.payment_service import MockYooKassaGateway


class OrderService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.cart_repository = CartRepository(session)
        self.order_repository = OrderRepository(session)
        self.payment_repository = PaymentRepository(session)
        self.payment_gateway = MockYooKassaGateway()

    async def create_from_cart(self, user_id: int | None, session_id: str | None, phone_number: str):
        if user_id is not None:
            cart = await self.cart_repository.get_active_for_user(user_id)
        else:
            if not session_id:
                raise BadRequestError("session_id is required for guest order")
            cart = await self.cart_repository.get_active_for_session(session_id)
        if cart is None or not cart.items:
            raise BadRequestError("Cart is empty")

        total_amount = sum((item.unit_price * item.quantity for item in cart.items), start=Decimal("0"))
        order = await self.order_repository.create(
            user_id=user_id,
            phone_number=phone_number,
            total_amount=total_amount,
        )
        for item in cart.items:
            await self.order_repository.create_item(
                order_id=order.id,
                dish_name=f"Dish #{item.dish_id}",
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        external_id, status = await self.payment_gateway.create_payment(total_amount)
        payment = await self.payment_repository.create(
            order_id=order.id, amount=total_amount, external_id=external_id
        )
        payment.status = status
        cart.is_active = False
        await self.session.commit()
        return await self.order_repository.get(order.id)

    async def list_my_orders(self, user_id: int, limit: int, offset: int):
        return await self.order_repository.list_for_user(user_id=user_id, limit=limit, offset=offset)

    async def list_all_orders(self, limit: int, offset: int, status: OrderStatus | None):
        return await self.order_repository.list_all(limit=limit, offset=offset, status=status)

    async def update_order_status(self, order_id: int, status: OrderStatus):
        order = await self.order_repository.get(order_id)
        if order is None:
            raise NotFoundError("Order not found")
        order.status = status
        await self.session.commit()
        await self.session.refresh(order)
        return await self.order_repository.get(order.id)
