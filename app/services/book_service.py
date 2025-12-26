from sqlalchemy.orm import Session
from typing import List
from app.models.book import Book


class BookService:
    """도서 관련 비즈니스 로직"""
    
    @staticmethod
    def get_popular_books(db: Session, limit: int = 10) -> List[Book]:
        """
        인기 도서 조회
        
        Args:
            db: 데이터베이스 세션
            limit: 조회할 도서 개수 (기본값: 10)
            
        Returns:
            인기 도서 목록
        """
        return db.query(Book)\
            .filter(Book.is_popular == True)\
            .order_by(Book.rating.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_theme_books(db: Session, theme: str, limit: int = 6) -> List[Book]:
        """
        테마별 도서 조회
        
        Args:
            db: 데이터베이스 세션
            theme: 테마 (work, healing, growth)
            limit: 조회할 도서 개수 (기본값: 6)
            
        Returns:
            테마별 도서 목록
        """
        return db.query(Book)\
            .filter(Book.theme == theme)\
            .order_by(Book.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_curator_picks(db: Session, limit: int = 6) -> List[Book]:
        """
        큐레이터 추천 도서 조회
        
        Args:
            db: 데이터베이스 세션
            limit: 조회할 도서 개수 (기본값: 6)
            
        Returns:
            큐레이터 추천 도서 목록
        """
        return db.query(Book)\
            .filter(Book.is_curator_pick == True)\
            .order_by(Book.rating.desc())\
            .limit(limit)\
            .all()
