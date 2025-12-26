"""
인증 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import timedelta
import re

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from app.schemas.auth import SignupRequest, SignupResponse, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: SignupRequest,
    db: Session = Depends(get_db)
):
    """
    회원가입
    
    - **email**: 이메일 주소
    - **password**: 비밀번호 (최소 8자)
    - **name**: 사용자 이름
    """
    # 이메일 중복 확인
    existing_user = AuthService.get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 사용자 생성
    user = AuthService.create_user(
        db=db,
        email=request.email,
        password=request.password,
        name=request.name
    )
    
    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return SignupResponse(
        success=True,
        message="User created successfully",
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at
        ),
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    로그인
    
    - **email**: 이메일 주소
    - **password**: 비밀번호
    """
    # 사용자 인증
    user = AuthService.authenticate_user(db, request.email, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return TokenResponse(
        success=True,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.get("/check-email")
def check_email(
    email: str = Query(..., description="확인할 이메일 주소"),
    db: Session = Depends(get_db)
):
    """
    이메일 중복 확인
    
    - **email**: 확인할 이메일 주소
    - **available**: true(사용 가능), false(이미 사용 중)
    """
    # 이메일 형식 검증
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # 이메일 중복 확인
    exists = AuthService.check_email_exists(db, email)
    
    if exists:
        return {
            "success": True,
            "available": False,
            "message": "이미 사용 중인 이메일입니다."
        }
    else:
        return {
            "success": True,
            "available": True,
            "message": "사용 가능한 이메일입니다."
        }
