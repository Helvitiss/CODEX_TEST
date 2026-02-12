from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.auth import OTPRequestSchema, OTPSentResponse, OTPVerifySchema, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/otp/request", response_model=OTPSentResponse)
async def request_otp(payload: OTPRequestSchema, session: AsyncSession = Depends(get_db_session)):
    service = AuthService(session)
    expires = await service.request_otp(payload.phone_number)
    return OTPSentResponse(phone_number=payload.phone_number, expires_in_seconds=expires)


@router.post("/otp/verify", response_model=TokenResponse)
async def verify_otp(payload: OTPVerifySchema, session: AsyncSession = Depends(get_db_session)):
    service = AuthService(session)
    token = await service.verify_otp_and_issue_token(payload.phone_number, payload.code)
    return TokenResponse(access_token=token)
