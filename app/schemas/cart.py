from decimal import Decimal

from pydantic import BaseModel, Field


class CartAddItem(BaseModel):
    dish_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemRead(BaseModel):
    id: int
    dish_id: int
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


class CartRead(BaseModel):
    id: int
    user_id: int | None
    session_id: str | None
    is_active: bool
    items: list[CartItemRead]

    model_config = {"from_attributes": True}
