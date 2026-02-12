from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, order_id: int, amount: Decimal, external_id: str | None) -> Payment:
        payment = Payment(order_id=order_id, amount=amount, external_id=external_id)
        self.session.add(payment)
        await self.session.flush()
        return payment
