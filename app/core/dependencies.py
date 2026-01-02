"""
FastAPI 의존성
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    JWT 토큰으로 현재 사용자 조회
    """
    token = credentials.credentials
    
    print(f"🔍 받은 토큰: {token[:50]}...")  # 디버깅
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        
        print(f"✅ 토큰 검증 성공, Email: {email}")  # 디버깅
        
        if email is None:
            print("❌ Email이 None입니다")  # 디버깅
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except JWTError as e:
        print(f"❌ JWT 에러: {e}")  # 디버깅
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        print(f"❌ 사용자를 찾을 수 없음: {email}")  # 디버깅
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    print(f"✅ 사용자 찾음: {user.email}")  # 디버깅
    return user
