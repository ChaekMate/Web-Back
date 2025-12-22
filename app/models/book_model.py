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
    cover_image = Column(String(500), nullable=True)  # 표지 이미지 URL
    description = Column(Text, nullable=True)
    
    # 가격 및 평점
    price = Column(Integer, nullable=True)  # 원 단위
    rating = Column(Float, default=0.0)  # 0.0 ~ 5.0
    review_count = Column(Integer, default=0)
    
    # 카테고리 및 태그
    theme = Column(String(50), nullable=True, index=True)  # 'work', 'healing', 'growth'
    category = Column(String(100), nullable=True)  # 장르 (예: 소설, 자기계발 등)
    keywords = Column(Text, nullable=True)  # 검색용 키워드 (쉼표 구분)
    
    # 특별 표시
    is_popular = Column(Boolean, default=False, index=True)  # 인기 도서
    is_curator_pick = Column(Boolean, default=False, index=True)  # 큐레이터 추천
    
    # 출판 정보
    published_date = Column(Date, nullable=True)
    page_count = Column(Integer, nullable=True)
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 (향후 추가)
    # reviews = relationship("Review", back_populates="book")
    # quotes = relationship("Quote", back_populates="book")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"