from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid


class User(Base):
    """사용자 모델"""
    __tablename__ = "users"
    
    # 기본 정보
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    
    # 상태
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # 이메일 인증 여부
    
    # 약관 동의
    agree_terms = Column(Boolean, default=False, nullable=False)
    agree_privacy = Column(Boolean, default=False, nullable=False)
    agree_marketing = Column(Boolean, default=False)
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    
    # 관계 (향후 추가)
    # conversations = relationship("Conversation", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"