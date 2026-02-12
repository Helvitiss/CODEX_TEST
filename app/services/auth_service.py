from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import BadRequestError
from app.core.security import create_access_token, generate_otp_code
from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.auth_repository = AuthRepository(session)
        self.user_repository = UserRepository(session)

    async def request_otp(self, phone_number: str) -> int:
        code = generate_otp_code()
        expires_at = datetime.now(UTC) + timedelta(seconds=settings.otp_ttl_seconds)
        await self.auth_repository.purge_phone_otps(phone_number)
        await self.auth_repository.create_otp(phone_number=phone_number, code=code, expires_at=expires_at)
        await self.session.commit()
        return settings.otp_ttl_seconds

    async def verify_otp_and_issue_token(self, phone_number: str, code: str) -> str:
        now = datetime.now(UTC)
        otp = await self.auth_repository.get_valid_otp(phone_number=phone_number, code=code, now=now)
        if otp is None:
            raise BadRequestError("Invalid or expired OTP")
        await self.auth_repository.purge_phone_otps(phone_number)
        user = await self.user_repository.get_by_phone(phone_number)
        if user is None:
            user = await self.user_repository.create(phone_number=phone_number)
        await self.session.commit()
        return create_access_token(subject=str(user.id), role=user.role.value)
