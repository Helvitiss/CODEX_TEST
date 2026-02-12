from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import OrderStatus


class CreateOrderRequest(BaseModel):
    phone_number: str = Field(min_length=8, max_length=20)


class OrderItemRead(BaseModel):
    id: int
    dish_name: str
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


class OrderRead(BaseModel):
    id: int
    user_id: int | None
    phone_number: str
    status: OrderStatus
    total_amount: Decimal
    items: list[OrderItemRead]

    model_config = {"from_attributes": True}


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus
