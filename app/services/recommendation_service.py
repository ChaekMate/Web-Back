"""
AI 추천 비즈니스 로직
"""

from sqlalchemy.orm import Session
from typing import List, Tuple
from app.models.book import Book
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
        
        Args:
            message: 사용자 메시지
            
        Returns:
            (테마, 추천 이유 템플릿) 튜플
        """
        message_lower = message.lower()
        
        # 키워드 매칭
        for keyword, theme in RecommendationService.KEYWORD_MAPPING.items():
            if keyword in message_lower:
                return theme, f"{keyword} 관련"
        
        # 기본값: healing (힐링)
        return "healing", "일상의 여유"
    
    @staticmethod
    def get_recommendations(
        db: Session,
        message: str,
        limit: int = 5
    ) -> Tuple[str, List[Book]]:
        """
        키워드 기반 도서 추천
        
        Args:
            db: 데이터베이스 세션
            message: 사용자 메시지
            limit: 추천할 도서 개수
            
        Returns:
            (AI 응답 메시지, 추천 도서 목록) 튜플
        """
        # 테마 추출
        theme, reason_template = RecommendationService.extract_theme_from_message(message)
        
        # 테마별 도서 조회 (평점 높은 순)
        books = db.query(Book)\
            .filter(Book.theme == theme)\
            .order_by(Book.rating.desc())\
            .limit(limit)\
            .all()
        
        # AI 응답 메시지 생성
        theme_messages = {
            "work": "업무와 자기계발에 도움이 되는 도서를 추천해드립니다.",
            "healing": "마음의 휴식과 위로를 줄 수 있는 도서를 추천해드립니다.",
            "growth": "지적 성장과 배움에 도움이 되는 도서를 추천해드립니다."
        }
        
        ai_message = theme_messages.get(theme, "다음 도서를 추천해드립니다.")
        
        return ai_message, books
