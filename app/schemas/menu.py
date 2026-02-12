from decimal import Decimal

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class CategoryRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class DishCreate(BaseModel):
    category_id: int
    name: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=2)
    price: Decimal = Field(gt=0)
    is_available: bool = True


class DishUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = Field(default=None, min_length=2)
    price: Decimal | None = Field(default=None, gt=0)
    is_available: bool | None = None


class DishRead(BaseModel):
    id: int
    category_id: int
    name: str
    description: str
    price: Decimal
    is_available: bool

    model_config = {"from_attributes": True}
