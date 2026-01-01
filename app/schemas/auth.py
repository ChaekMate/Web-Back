"""
인증 관련 스키마
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class SignupRequest(BaseModel):
    """회원가입 요청"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str
    agree_terms: bool = True
    agree_privacy: bool = True
    agree_marketing: bool = False


class LoginRequest(BaseModel):
    """로그인 요청"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """사용자 응답"""
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class SignupResponse(BaseModel):
    """회원가입 응답"""
    success: bool
    message: str
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenResponse(BaseModel):
    """토큰 응답"""
    success: bool
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
