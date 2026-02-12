from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.dependencies.auth import get_current_admin
from app.schemas.menu import DishRead
from app.services.dish_image_service import DishImageService

router = APIRouter(prefix="/admin/dishes", tags=["admin-dishes"], dependencies=[Depends(get_current_admin)])


@router.post("/{dish_id}/image", response_model=DishRead)
async def upload_dish_image(
    dish_id: int,
    image: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session),
):
    return await DishImageService(session).upload_image(dish_id=dish_id, upload_file=image)
