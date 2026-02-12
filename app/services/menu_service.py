from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, NotFoundError
from app.repositories.menu_repository import CategoryRepository, DishRepository
from app.schemas.menu import CategoryCreate, CategoryUpdate, DishCreate, DishUpdate


class MenuService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.category_repository = CategoryRepository(session)
        self.dish_repository = DishRepository(session)

    async def create_category(self, payload: CategoryCreate):
        category = await self.category_repository.create(name=payload.name)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def update_category(self, category_id: int, payload: CategoryUpdate):
        category = await self.category_repository.get(category_id)
        if category is None:
            raise NotFoundError("Category not found")
        category.name = payload.name
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete_category(self, category_id: int) -> None:
        category = await self.category_repository.get(category_id)
        if category is None:
            raise NotFoundError("Category not found")
        await self.category_repository.delete(category)
        await self.session.commit()

    async def list_categories(self, limit: int, offset: int):
        return await self.category_repository.list(limit=limit, offset=offset)

    async def create_dish(self, payload: DishCreate):
        category = await self.category_repository.get(payload.category_id)
        if category is None:
            raise BadRequestError("Category does not exist")
        dish = await self.dish_repository.create(data=payload.model_dump())
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def update_dish(self, dish_id: int, payload: DishUpdate):
        dish = await self.dish_repository.get(dish_id)
        if dish is None:
            raise NotFoundError("Dish not found")
        update_data = payload.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            category = await self.category_repository.get(update_data["category_id"])
            if category is None:
                raise BadRequestError("Category does not exist")
        for key, value in update_data.items():
            setattr(dish, key, value)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def delete_dish(self, dish_id: int) -> None:
        dish = await self.dish_repository.get(dish_id)
        if dish is None:
            raise NotFoundError("Dish not found")
        await self.dish_repository.delete(dish)
        await self.session.commit()

    async def list_dishes(self, limit: int, offset: int, category_id: int | None, is_available: bool | None):
        return await self.dish_repository.list(
            limit=limit,
            offset=offset,
            category_id=category_id,
            is_available=is_available,
        )
