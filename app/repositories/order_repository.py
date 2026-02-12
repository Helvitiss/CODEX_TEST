from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import OrderStatus
from app.models.order import Order, OrderItem


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int | None, phone_number: str, total_amount: Decimal) -> Order:
        order = Order(user_id=user_id, phone_number=phone_number, total_amount=total_amount)
        self.session.add(order)
        await self.session.flush()
        return order

    async def create_item(self, order_id: int, dish_name: str, quantity: int, unit_price: Decimal) -> OrderItem:
        item = OrderItem(order_id=order_id, dish_name=dish_name, quantity=quantity, unit_price=unit_price)
        self.session.add(item)
        await self.session.flush()
        return item

    async def get(self, order_id: int) -> Order | None:
        result = await self.session.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        return result.scalar_one_or_none()

    async def list_for_user(self, user_id: int, limit: int, offset: int) -> list[Order]:
        result = await self.session.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def list_all(
        self, limit: int, offset: int, status: OrderStatus | None = None
    ) -> list[Order]:
        query = select(Order).options(selectinload(Order.items)).order_by(Order.id.desc())
        if status is not None:
            query = query.where(Order.status == status)
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().all())
