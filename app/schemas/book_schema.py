from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# ========== 기본 스키마 ==========

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


# ========== API 응답 스키마 ==========

class BookResponse(BookBase):
    """도서 목록 응답 (간단한 정보)"""
    pass


class BookDetailResponse(BookDetail):
    """도서 상세 응답 (전체 정보)"""
    pass


class BookListResponse(BaseModel):
    """도서 목록 응답"""
    books: List[BookResponse]
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


# ========== AI 추천용 스키마 ==========

class RecommendedBook(BookBase):
    """AI 추천 도서 (추천 이유 포함)"""
    reason: str  # AI가 추천한 이유
    match_score: Optional[float] = None  # 매칭 점수 (0.0 ~ 1.0)


class RecommendedBookList(BaseModel):
    """AI 추천 도서 목록"""
    books: List[RecommendedBook]
    explanation: Optional[str] = None  # 전체 추천 설명


# ========== 생성/수정 스키마 (관리자용 - 향후 사용) ==========

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
    isbn: Optional[str] = Field(None, max_length=20)
    cover_image: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    theme: Optional[str] = Field(None, pattern="^(work|healing|growth)$")
    category: Optional[str] = None
    is_popular: Optional[bool] = None
    is_curator_pick: Optional[bool] = None