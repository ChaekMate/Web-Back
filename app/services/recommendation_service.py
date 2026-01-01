"""
AI 추천 비즈니스 로직
"""

from sqlalchemy.orm import Session
from typing import List, Tuple
from app.models.book import Book
from app.models.recommendation_history import RecommendationHistory
from app.models.user import User
import re


class RecommendationService:
    """AI 추천 관련 비즈니스 로직"""
    
    # 키워드 매핑
    KEYWORD_MAPPING = {
        "업무": "work",
        "일": "work",
        "비즈니스": "work",
        "경영": "work",
        "자기계발": "work",
        "생산성": "work",
        "효율": "work",
        "힐링": "healing",
        "위로": "healing",
        "휴식": "healing",
        "소설": "healing",
        "에세이": "healing",
        "감성": "healing",
        "스트레스": "healing",
        "성장": "growth",
        "인문": "growth",
        "철학": "growth",
        "역사": "growth",
        "과학": "growth",
        "심리": "growth",
        "배움": "growth"
    }
    
    @staticmethod
    def extract_theme_from_message(message: str) -> Tuple[str, str]:
        """
        메시지에서 테마 추출
        """
        message_lower = message.lower()
        
        for keyword, theme in RecommendationService.KEYWORD_MAPPING.items():
            if keyword in message_lower:
                return theme, f"{keyword} 관련"
        
        return "healing", "일상의 여유"
    
    @staticmethod
    def get_recommendations(
        db: Session,
        message: str,
        limit: int = 5
    ) -> Tuple[str, List[Book], str]:
        """
        키워드 기반 도서 추천
        
        Returns:
            (AI 응답 메시지, 추천 도서 목록, 테마) 튜플
        """
        theme, reason_template = RecommendationService.extract_theme_from_message(message)
        
        books = db.query(Book)\
            .filter(Book.theme == theme)\
            .order_by(Book.rating.desc())\
            .limit(limit)\
            .all()
        
        theme_messages = {
            "work": "업무와 자기계발에 도움이 되는 도서를 추천해드립니다.",
            "healing": "마음의 휴식과 위로를 줄 수 있는 도서를 추천해드립니다.",
            "growth": "지적 성장과 배움에 도움이 되는 도서를 추천해드립니다."
        }
        
        ai_message = theme_messages.get(theme, "다음 도서를 추천해드립니다.")
        
        return ai_message, books, theme
    
    @staticmethod
    def save_history(
        db: Session,
        user: User,
        user_message: str,
        ai_response: str,
        book_ids: List[int],
        theme: str
    ) -> RecommendationHistory:
        """
        추천 히스토리 저장
        """
        history = RecommendationHistory(
            user_id=user.id,
            user_message=user_message,
            ai_response=ai_response,
            recommended_book_ids=",".join(map(str, book_ids)),
            theme=theme
        )
        
        db.add(history)
        db.commit()
        db.refresh(history)
        
        return history
    
    @staticmethod
    def get_user_histories(
        db: Session,
        user: User,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[RecommendationHistory], int]:
        """
        사용자 추천 히스토리 조회
        """
        total = db.query(RecommendationHistory)\
            .filter(RecommendationHistory.user_id == user.id)\
            .count()
        
        histories = db.query(RecommendationHistory)\
            .filter(RecommendationHistory.user_id == user.id)\
            .order_by(RecommendationHistory.created_at.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        return histories, total
    
    @staticmethod
    def get_history_by_id(
        db: Session,
        user: User,
        history_id: int
    ) -> RecommendationHistory:
        """
        특정 히스토리 조회
        """
        return db.query(RecommendationHistory)\
            .filter(
                RecommendationHistory.id == history_id,
                RecommendationHistory.user_id == user.id
            )\
            .first()
