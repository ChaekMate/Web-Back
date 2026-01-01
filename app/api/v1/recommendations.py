"""
AI 추천 API 엔드포인트
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.recommendation_service import RecommendationService
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendedBookResponse
)

router = APIRouter()


@router.post("/chat", response_model=RecommendationResponse)
def chat_recommendation(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """AI 추천 채팅"""
    
    ai_message, books, theme = RecommendationService.get_recommendations(
        db=db,
        message=request.message,
        limit=5
    )
    
    theme_reasons = {
        "work": "업무 효율과 성과 향상에 도움",
        "healing": "마음의 휴식과 위로 제공",
        "growth": "지적 성장과 통찰력 향상"
    }
    
    recommended_books = [
        RecommendedBookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            cover_image=book.cover_image,
            description=book.description,
            price=book.price,
            rating=book.rating,
            theme=book.theme,
            reason=theme_reasons.get(book.theme, "추천 도서")
        )
        for book in books
    ]
    
    return RecommendationResponse(
        success=True,
        message=ai_message,
        books=recommended_books
    )
