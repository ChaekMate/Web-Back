"""
AI 추천 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.book import Book
from app.services.recommendation_service import RecommendationService
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendedBookResponse
)
from app.schemas.history import (
    RecommendationHistoryResponse,
    RecommendationHistoryListResponse
)

router = APIRouter()


@router.post("/chat", response_model=RecommendationResponse)
def chat_recommendation(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """AI 추천 채팅 (로그인 필수)"""
    
    # AI 추천
    ai_message, books, theme = RecommendationService.get_recommendations(
        db=db,
        message=request.message,
        limit=5
    )
    
    # 히스토리 저장
    book_ids = [book.id for book in books]
    RecommendationService.save_history(
        db=db,
        user=current_user,
        user_message=request.message,
        ai_response=ai_message,
        book_ids=book_ids,
        theme=theme
    )
    
    # 추천 이유 생성
    theme_reasons = {
        "work": "업무 효율과 성과 향상에 도움",
        "healing": "마음의 휴식과 위로 제공",
        "growth": "지적 성장과 통찰력 향상"
    }
    
    # 응답 데이터 생성
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


@router.get("/history", response_model=RecommendationHistoryListResponse)
def get_recommendation_history(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """추천 히스토리 조회 (로그인 필수)"""
    
    histories, total = RecommendationService.get_user_histories(
        db=db,
        user=current_user,
        limit=limit,
        offset=offset
    )
    
    return RecommendationHistoryListResponse(
        success=True,
        total=total,
        data=histories
    )


@router.get("/history/{history_id}")
def get_recommendation_history_detail(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """특정 추천 히스토리 상세 조회 (로그인 필수)"""
    
    history = RecommendationService.get_history_by_id(
        db=db,
        user=current_user,
        history_id=history_id
    )
    
    if not history:
        raise HTTPException(
            status_code=404,
            detail="History not found"
        )
    
    # 추천된 도서 조회
    book_ids = [int(id) for id in history.recommended_book_ids.split(",") if id]
    books = db.query(Book).filter(Book.id.in_(book_ids)).all() if book_ids else []
    
    return {
        "success": True,
        "data": {
            "id": history.id,
            "user_message": history.user_message,
            "ai_response": history.ai_response,
            "theme": history.theme,
            "created_at": history.created_at,
            "books": [
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "cover_image": book.cover_image,
                    "price": book.price,
                    "rating": book.rating
                }
                for book in books
            ]
        }
    }
