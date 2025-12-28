"""
도서 모델
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base


class Book(Base):
    """도서 테이블"""
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(500), nullable=False, index=True)
    author = Column(String(200), nullable=False)
    publisher = Column(String(200))
    isbn = Column(String(20), unique=True, index=True)
    cover_image = Column(String(500))
    description = Column(Text)
    price = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    theme = Column(String(50), index=True)
    category = Column(String(100))
    keywords = Column(String(500))
    is_popular = Column(Boolean, default=False, index=True)
    is_curator_pick = Column(Boolean, default=False, index=True)
    published_date = Column(Date)
    page_count = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
