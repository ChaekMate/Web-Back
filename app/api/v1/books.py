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
        "theme": book.theme,
        "is_popular": book.is_popular,
        "is_curator_pick": book.is_curator_pick
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
