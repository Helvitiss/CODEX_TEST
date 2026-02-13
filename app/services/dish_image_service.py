from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.storage import LocalFileStorage
from app.repositories.menu_repository import DishRepository

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


class DishImageService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.dish_repository = DishRepository(session)
        media_dir = Path(settings.media_root) / settings.dish_media_subdir
        self.storage = LocalFileStorage(destination_dir=media_dir, public_prefix=f"/media/{settings.dish_media_subdir}")

    async def upload_image(self, dish_id: int, upload_file: UploadFile):
        dish = await self.dish_repository.get(dish_id)
        if dish is None:
            raise NotFoundError("Dish not found")

        if upload_file.content_type not in ALLOWED_IMAGE_TYPES:
            raise BadRequestError("Unsupported image type. Allowed types: jpeg, png, webp")

        image_path = await self.storage.save_file(upload_file)
        await self.dish_repository.update_image_path(dish=dish, image_path=image_path)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish
