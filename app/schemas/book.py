"""
도서 관련 Pydantic 스키마
요청/응답 데이터 검증
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class BookBase(BaseModel):
    """도서 기본 정보"""
    id: str
    title: str
    author: str
    publisher: Optional[str] = None
    cover_image: Optional[str] = None
    price: Optional[int] = None
    rating: Optional[float] = 0.0
    
    class Config:
        from_attributes = True


class BookDetail(BookBase):
    """도서 상세 정보"""
    isbn: Optional[str] = None
    description: Optional[str] = None
    review_count: int = 0
    theme: Optional[str] = None
    category: Optional[str] = None
    keywords: Optional[str] = None
    published_date: Optional[date] = None
    page_count: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class BookResponse(BookBase):
    """도서 목록 응답"""
    pass


class BookDetailResponse(BookDetail):
    """도서 상세 응답"""
    pass


class BookListResponse(BaseModel):
    """도서 목록 응답"""
    books: List[BookResponse]
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class RecommendedBook(BookBase):
    """AI 추천 도서"""
    reason: str
    match_score: Optional[float] = None


class RecommendedBookList(BaseModel):
    """AI 추천 도서 목록"""
    books: List[RecommendedBook]
    explanation: Optional[str] = None


class BookCreate(BaseModel):
    """도서 생성"""
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=200)
    publisher: Optional[str] = Field(None, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    cover_image: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)
    theme: Optional[str] = Field(None, pattern="^(work|healing|growth)$")
    category: Optional[str] = None
    published_date: Optional[date] = None
    page_count: Optional[int] = Field(None, ge=1)


class BookUpdate(BaseModel):
    """도서 수정"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    publisher: Optional[str] = Field(None, max_length=200)
    price: Optional[int] = Field(None, ge=0)
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    theme: Optional[str] = Field(None, pattern="^(work|healing|growth)$")
    is_popular: Optional[bool] = None
    is_curator_pick: Optional[bool] = None
