"""
도서 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.book import Book
from app.services.book_service import BookService

router = APIRouter()

# 허용된 테마 목록
ALLOWED_THEMES = ["work", "healing", "growth"]


def serialize_book(book: Book) -> dict:
    """Book 모델을 딕셔너리로 변환"""
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "isbn": book.isbn,
        "cover_image": book.cover_image,
        "description": book.description,
        "price": book.price,
        "rating": book.rating,
        "review_count": book.review_count,
        "theme": book.theme,
        "category": book.category,
        "is_popular": book.is_popular,
        "is_curator_pick": book.is_curator_pick,
        "published_date": str(book.published_date) if book.published_date else None,
        "page_count": book.page_count
    }


@router.get("/all")
def get_all_books(db: Session = Depends(get_db)):
    """전체 도서 목록 조회"""
    books = db.query(Book).all()
    
    return {
        "success": True,
        "data": [serialize_book(book) for book in books]
    }


@router.get("/popular")
def get_popular_books(
    limit: int = Query(default=10, ge=1, le=50, description="조회할 도서 개수"),
    db: Session = Depends(get_db)
):
    """
    인기 도서 조회
    
    - **limit**: 조회할 도서 개수 (기본값: 10, 최대: 50)
    """
    books = BookService.get_popular_books(db, limit)
    
    return {
        "success": True,
        "data": [serialize_book(book) for book in books]
    }


@router.get("/theme/{theme}")
def get_theme_books(
    theme: str,
    limit: int = Query(default=6, ge=1, le=50, description="조회할 도서 개수"),
    db: Session = Depends(get_db)
):
    """
    테마별 도서 조회
    
    - **theme**: 테마 (work, healing, growth)
    - **limit**: 조회할 도서 개수 (기본값: 6, 최대: 50)
    """
    # 테마 유효성 검사
    if theme not in ALLOWED_THEMES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid theme. Allowed themes: {', '.join(ALLOWED_THEMES)}"
        )
    
    books = BookService.get_theme_books(db, theme, limit)
    
    return {
        "success": True,
        "data": [serialize_book(book) for book in books]
    }


@router.get("/curator-picks")
def get_curator_picks(
    limit: int = Query(default=6, ge=1, le=50, description="조회할 도서 개수"),
    db: Session = Depends(get_db)
):
    """
    큐레이터 추천 도서 조회
    
    - **limit**: 조회할 도서 개수 (기본값: 6, 최대: 50)
    """
    books = BookService.get_curator_picks(db, limit)
    
    return {
        "success": True,
        "data": [serialize_book(book) for book in books]
    }


@router.get("/search")
def search_books(
    q: str = Query(..., description="검색 키워드"),
    limit: int = Query(default=20, ge=1, le=100, description="조회할 도서 개수"),
    offset: int = Query(default=0, ge=0, description="건너뛸 개수"),
    db: Session = Depends(get_db)
):
    """
    도서 검색
    
    - **q**: 검색 키워드 (제목, 저자, 출판사 검색)
    - **limit**: 조회할 도서 개수 (기본값: 20, 최대: 100)
    - **offset**: 건너뛸 개수 (페이지네이션용, 기본값: 0)
    """
    books, total = BookService.search_books(db, q, limit, offset)
    
    return {
        "success": True,
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": [serialize_book(book) for book in books]
    }


@router.get("/{book_id}")
def get_book_detail(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    도서 상세 조회
    
    - **book_id**: 도서 ID
    """
    book = BookService.get_book_by_id(db, book_id)
    
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    return {
        "success": True,
        "data": serialize_book(book)
    }
