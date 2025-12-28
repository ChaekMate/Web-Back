"""
도서 비즈니스 로직
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
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
    
    @staticmethod
    def search_books(
        db: Session,
        query: str,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Book], int]:
        """
        도서 검색
        
        Args:
            db: 데이터베이스 세션
            query: 검색 키워드
            limit: 조회할 도서 개수 (기본값: 20)
            offset: 건너뛸 개수 (기본값: 0)
            
        Returns:
            (도서 목록, 전체 개수) 튜플
        """
        # 검색 쿼리 (대소문자 구분 없음)
        search_filter = or_(
            func.lower(Book.title).contains(query.lower()),
            func.lower(Book.author).contains(query.lower()),
            func.lower(Book.publisher).contains(query.lower())
        )
        
        # 전체 개수
        total = db.query(Book).filter(search_filter).count()
        
        # 검색 결과
        books = db.query(Book)\
            .filter(search_filter)\
            .order_by(Book.rating.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        return books, total
    
    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
        """
        ID로 도서 상세 조회
        
        Args:
            db: 데이터베이스 세션
            book_id: 도서 ID
            
        Returns:
            Book 객체 또는 None
        """
        return db.query(Book).filter(Book.id == book_id).first()
