from datetime import UTC, datetime, timedelta
from random import randint

from jose import jwt

from app.core.config import settings


def create_access_token(subject: str, role: str) -> str:
    expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    expire = datetime.now(UTC) + expires_delta
    payload = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def generate_otp_code() -> str:
    return f"{randint(0, 999999):06d}"
