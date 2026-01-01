"""
추천 히스토리 모델
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class RecommendationHistory(Base):
    """추천 히스토리 테이블"""
    __tablename__ = "recommendation_histories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    recommended_book_ids = Column(String(500))  # 쉼표로 구분된 도서 ID
    theme = Column(String(50))  # 추천된 테마
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    # Relationship
    user = relationship("User", back_populates="recommendation_histories")
