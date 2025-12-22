from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ========== 회원가입 ==========

class SignupRequest(BaseModel):
    """회원가입 요청"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: Optional[str] = Field(None, max_length=50)
    agree_terms: bool
    agree_privacy: bool
    agree_marketing: bool = False


class SignupResponse(BaseModel):
    """회원가입 응답"""
    id: str
    email: str
    name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== 로그인 ==========

class LoginRequest(BaseModel):
    """로그인 요청"""
    email: EmailStr
    password: str
    remember: bool = False


class TokenResponse(BaseModel):
    """토큰 응답"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int  # seconds
    user: "UserResponse"


class RefreshTokenRequest(BaseModel):
    """토큰 갱신 요청"""
    refresh_token: str


# ========== 사용자 정보 ==========

class UserResponse(BaseModel):
    """사용자 정보 응답"""
    id: str
    email: str
    name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """사용자 정보 수정"""
    name: Optional[str] = Field(None, max_length=50)
    

# ========== 공통 응답 ==========

class MessageResponse(BaseModel):
    """메시지 응답"""
    message: str