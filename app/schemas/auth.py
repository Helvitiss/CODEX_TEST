from pydantic import BaseModel, Field


class OTPRequestSchema(BaseModel):
    phone_number: str = Field(min_length=8, max_length=20)


class OTPVerifySchema(BaseModel):
    phone_number: str = Field(min_length=8, max_length=20)
    code: str = Field(min_length=6, max_length=6)


class OTPSentResponse(BaseModel):
    phone_number: str
    expires_in_seconds: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
