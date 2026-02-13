from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu import Category, Dish


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, name: str) -> Category:
        category = Category(name=name)
        self.session.add(category)
        await self.session.flush()
        return category

    async def get(self, category_id: int) -> Category | None:
        result = await self.session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def list(self, limit: int, offset: int) -> list[Category]:
        result = await self.session.execute(select(Category).limit(limit).offset(offset).order_by(Category.id))
        return list(result.scalars().all())

    async def delete(self, category: Category) -> None:
        await self.session.delete(category)


class DishRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: dict) -> Dish:
        dish = Dish(**data)
        self.session.add(dish)
        await self.session.flush()
        return dish

    async def get(self, dish_id: int) -> Dish | None:
        result = await self.session.execute(select(Dish).where(Dish.id == dish_id))
        return result.scalar_one_or_none()

    async def list(
        self, limit: int, offset: int, category_id: int | None = None, is_available: bool | None = None
    ) -> list[Dish]:
        conditions = []
        if category_id is not None:
            conditions.append(Dish.category_id == category_id)
        if is_available is not None:
            conditions.append(Dish.is_available == is_available)
        query = select(Dish)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.limit(limit).offset(offset).order_by(Dish.id)
        result = await self.session.execute(query)
        return list(result.scalars().all())


    async def update_image_path(self, dish: Dish, image_path: str) -> Dish:
        dish.image_path = image_path
        await self.session.flush()
        return dish

    async def delete(self, dish: Dish) -> None:
        await self.session.delete(dish)
