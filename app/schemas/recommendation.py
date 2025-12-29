"""
AI 추천 관련 스키마
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """채팅 메시지"""
    role: str = Field(..., description="메시지 역할 (user/assistant)")
    content: str = Field(..., description="메시지 내용")


class RecommendationRequest(BaseModel):
    """추천 요청"""
    message: str = Field(..., min_length=1, max_length=1000, description="사용자 메시지")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "업무 스트레스를 풀 수 있는 힐링 도서 추천해줘"
            }
        }


class RecommendedBookResponse(BaseModel):
    """추천 도서 정보"""
    id: int
    title: str
    author: str
    cover_image: Optional[str]
    description: Optional[str]
    price: Optional[int]
    rating: float
    theme: str
    reason: str = Field(..., description="추천 이유")


class RecommendationResponse(BaseModel):
    """추천 응답"""
    success: bool
    message: str = Field(..., description="AI 응답 메시지")
    books: List[RecommendedBookResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "업무 스트레스 해소에 도움이 되는 힐링 도서를 추천해드립니다.",
                "books": []
            }
        }
