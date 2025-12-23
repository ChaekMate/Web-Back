"""
Book 모델
도서 정보 저장
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, Date, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid


class Book(Base):
    """도서 모델"""
    __tablename__ = "books"
    
    # 기본 정보
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False, index=True)
    author = Column(String(200), nullable=False, index=True)
    publisher = Column(String(200), nullable=True)
    isbn = Column(String(20), unique=True, nullable=True, index=True)
    
    # 이미지 및 설명
    cover_image = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    
    # 가격 및 평점
    price = Column(Integer, nullable=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    
    # 카테고리 및 태그
    theme = Column(String(50), nullable=True, index=True)
    category = Column(String(100), nullable=True)
    keywords = Column(Text, nullable=True)
    
    # 특별 표시
    is_popular = Column(Boolean, default=False, index=True)
    is_curator_pick = Column(Boolean, default=False, index=True)
    
    # 출판 정보
    published_date = Column(Date, nullable=True)
    page_count = Column(Integer, nullable=True)
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"
