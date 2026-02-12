from decimal import Decimal

from pydantic import BaseModel

from app.models.enums import PaymentStatus


class PaymentRead(BaseModel):
    id: int
    order_id: int
    amount: Decimal
    status: PaymentStatus
    external_id: str | None

    model_config = {"from_attributes": True}
