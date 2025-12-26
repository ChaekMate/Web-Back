"""
인증 관련 비즈니스 로직
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from datetime import datetime


class AuthService:
    """인증 관련 비즈니스 로직"""
    
    @staticmethod
    def create_user(db: Session, email: str, password: str, name: str) -> User:
        """
        새 사용자 생성
        
        Args:
            db: 데이터베이스 세션
            email: 이메일
            password: 비밀번호 (평문)
            name: 이름
            
        Returns:
            생성된 User 객체
        """
        hashed_password = get_password_hash(password)
        
        user = User(
            email=email.lower(),
            hashed_password=hashed_password,
            name=name
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """
        사용자 인증
        
        Args:
            db: 데이터베이스 세션
            email: 이메일
            password: 비밀번호 (평문)
            
        Returns:
            인증된 User 객체 또는 None
        """
        user = db.query(User).filter(User.email == email.lower()).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """
        이메일로 사용자 조회
        
        Args:
            db: 데이터베이스 세션
            email: 이메일
            
        Returns:
            User 객체 또는 None
        """
        return db.query(User).filter(User.email == email.lower()).first()
    
    @staticmethod
    def check_email_exists(db: Session, email: str) -> bool:
        """
        이메일 중복 확인
        
        Args:
            db: 데이터베이스 세션
            email: 확인할 이메일
            
        Returns:
            True: 이메일 존재, False: 사용 가능
        """
        user = db.query(User).filter(User.email == email.lower()).first()
        return user is not None
