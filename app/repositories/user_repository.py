from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone_number: str) -> User | None:
        result = await self.session.execute(select(User).where(User.phone_number == phone_number))
        return result.scalar_one_or_none()

    async def create(self, phone_number: str) -> User:
        user = User(phone_number=phone_number)
        self.session.add(user)
        await self.session.flush()
        return user
