from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import OTPCode


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_otp(self, phone_number: str, code: str, expires_at: datetime) -> OTPCode:
        otp = OTPCode(phone_number=phone_number, code=code, expires_at=expires_at)
        self.session.add(otp)
        await self.session.flush()
        return otp

    async def purge_phone_otps(self, phone_number: str) -> None:
        await self.session.execute(delete(OTPCode).where(OTPCode.phone_number == phone_number))

    async def get_valid_otp(self, phone_number: str, code: str, now: datetime) -> OTPCode | None:
        result = await self.session.execute(
            select(OTPCode).where(
                OTPCode.phone_number == phone_number,
                OTPCode.code == code,
                OTPCode.expires_at > now,
            )
        )
        return result.scalar_one_or_none()
