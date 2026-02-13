import asyncio
from decimal import Decimal
from random import Random

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, engine
from app.models import Base
from app.models.menu import Category, Dish

CATEGORY_NAMES = [
    "Burgers",
    "Pizza",
    "Sushi",
    "Salads",
    "Desserts",
    "Drinks",
]

ADJECTIVES = [
    "Spicy",
    "Crispy",
    "Classic",
    "Smoky",
    "Double",
    "Herb",
    "Signature",
    "Golden",
]

ITEMS = [
    "Chicken Burger",
    "Veggie Burger",
    "Cheese Pizza",
    "Pepperoni Pizza",
    "Dragon Roll",
    "California Roll",
    "Greek Salad",
    "Caesar Salad",
    "Cheesecake",
    "Chocolate Brownie",
    "Lemonade",
    "Iced Tea",
]


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    rng = Random(42)

    async with AsyncSessionLocal() as session:
        existing_categories_result = await session.execute(select(Category))
        existing_categories = {category.name: category for category in existing_categories_result.scalars().all()}

        for name in CATEGORY_NAMES:
            if name not in existing_categories:
                category = Category(name=name)
                session.add(category)
                existing_categories[name] = category

        await session.flush()

        categories = list(existing_categories.values())
        existing_dishes_result = await session.execute(select(Dish.name))
        existing_dish_names = set(existing_dishes_result.scalars().all())

        generated = []
        index = 1
        while len(generated) < 30:
            dish_name = f"{rng.choice(ADJECTIVES)} {rng.choice(ITEMS)}"
            if dish_name in existing_dish_names or dish_name in {d['name'] for d in generated}:
                dish_name = f"{dish_name} {index}"
            generated.append(
                {
                    "name": dish_name,
                    "description": f"Freshly prepared {dish_name.lower()} with premium ingredients.",
                    "price": Decimal(str(round(rng.uniform(4.5, 24.9), 2))),
                    "category_id": categories[len(generated) % len(categories)].id,
                    "image_path": f"/media/dishes/sample_{index:02d}.webp",
                    "is_available": True,
                }
            )
            index += 1

        for dish_data in generated:
            if dish_data["name"] not in existing_dish_names:
                session.add(Dish(**dish_data))

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
