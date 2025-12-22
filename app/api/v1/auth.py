from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def register(
    signup_data: SignupRequest,
    db: Session = Depends(get_db)
):
    """
    회원가입
    
    - **email**: 이메일 (필수, 중복 불가)
    - **password**: 비밀번호 (필수, 8자 이상)
    - **name**: 이름 (선택)
    - **agree_terms**: 이용약관 동의 (필수)
    - **agree_privacy**: 개인정보 처리방침 동의 (필수)
    - **agree_marketing**: 마케팅 수신 동의 (선택)
    """
    user = AuthService.create_user(db, signup_data)
    
    return SignupResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    로그인
    
    - **email**: 이메일
    - **password**: 비밀번호
    - **remember**: 로그인 유지 (True: 7일, False: 30분)
    """
    # 사용자 인증
    user = AuthService.authenticate_user(
        db,
        login_data.email,
        login_data.password
    )
    
    # 토큰 생성
    tokens = AuthService.create_tokens(user, login_data.remember)
    
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="Bearer",
        expires_in=tokens["expires_in"],
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at
        )
    )


@router.post("/refresh")
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Access Token 갱신
    
    Refresh Token을 사용하여 새로운 Access Token 발급
    """
    new_token = AuthService.refresh_access_token(db, refresh_data.refresh_token)
    return new_token


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    현재 사용자 정보 조회
    
    인증 헤더: Authorization: Bearer {access_token}
    """
    token = credentials.credentials
    user = AuthService.get_current_user(db, token)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at
    )


@router.post("/logout")
async def logout():
    """
    로그아웃
    
    클라이언트에서 토큰 삭제 필요
    (서버에서는 Stateless이므로 별도 처리 없음)
    """
    return {"message": "로그아웃되었습니다"}