from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.book import Book
from app.schemas.book import BookResponse

router = APIRouter()


@router.get("/all", response_model=dict)
def get_all_books(db: Session = Depends(get_db)):
    """전체 도서 목록 조회"""
    books = db.query(Book).all()
    
    return {
        "success": True,
        "data": [
            {
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
            for book in books
        ]
    }
