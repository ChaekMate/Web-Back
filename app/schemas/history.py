"""
추천 히스토리 관련 스키마
"""

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class RecommendationHistoryResponse(BaseModel):
    """추천 히스토리 응답"""
    id: int
    user_message: str
    ai_response: str
    recommended_book_ids: str
    theme: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecommendationHistoryListResponse(BaseModel):
    """추천 히스토리 목록 응답"""
    success: bool
    total: int
    data: List[RecommendationHistoryResponse]
