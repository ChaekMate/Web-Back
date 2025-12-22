from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.config import settings


class AuthService:
    """인증 서비스 클래스"""
    
    @staticmethod
    def create_user(db: Session, signup_data: SignupRequest) -> User:
        """
        회원가입
        
        Args:
            db: 데이터베이스 세션
            signup_data: 회원가입 데이터
            
        Returns:
            User: 생성된 사용자
            
        Raises:
            HTTPException: 이메일 중복 시
        """
        # 이메일 중복 체크
        existing_user = db.query(User).filter(User.email == signup_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 이메일입니다"
            )
        
        # 비밀번호 해싱
        hashed_password = get_password_hash(signup_data.password)
        
        # 사용자 생성
        new_user = User(
            email=signup_data.email,
            hashed_password=hashed_password,
            name=signup_data.name,
            agree_terms=signup_data.agree_terms,
            agree_privacy=signup_data.agree_privacy,
            agree_marketing=signup_data.agree_marketing,
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """
        사용자 인증
        
        Args:
            db: 데이터베이스 세션
            email: 이메일
            password: 비밀번호
            
        Returns:
            User: 인증된 사용자
            
        Raises:
            HTTPException: 인증 실패 시
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다"
            )
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="비활성화된 계정입니다"
            )
        
        # 마지막 로그인 시간 업데이트
        user.last_login_at = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def create_tokens(user: User, remember: bool = False) -> dict:
        """
        토큰 생성
        
        Args:
            user: 사용자
            remember: 로그인 유지 여부
            
        Returns:
            dict: access_token, refresh_token
        """
        # 토큰 페이로드
        token_data = {"sub": user.id, "email": user.email}
        
        # Access Token
        if remember:
            # 로그인 유지 시 7일
            expires_delta = timedelta(days=7)
        else:
            expires_delta = None  # 기본값 30분
        
        access_token = create_access_token(token_data, expires_delta)
        
        # Refresh Token
        refresh_token = create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 if not remember else 7 * 24 * 60 * 60
        }
    
    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        """
        토큰으로 현재 사용자 조회
        
        Args:
            db: 데이터베이스 세션
            token: JWT 토큰
            
        Returns:
            User: 현재 사용자
            
        Raises:
            HTTPException: 토큰 검증 실패 시
        """
        payload = decode_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다"
            )
        
        return user
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> dict:
        """
        Access Token 갱신
        
        Args:
            db: 데이터베이스 세션
            refresh_token: Refresh Token
            
        Returns:
            dict: 새로운 access_token
        """
        payload = decode_token(refresh_token)
        
        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 Refresh Token입니다"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다"
            )
        
        # 새 Access Token 생성
        token_data = {"sub": user.id, "email": user.email}
        new_access_token = create_access_token(token_data)
        
        return {
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }