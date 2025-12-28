"""
도서 비교 관련 스키마
"""

from pydantic import BaseModel, Field, field_validator
from typing import List


class BookCompareRequest(BaseModel):
    """도서 비교 요청"""
    book_ids: List[int] = Field(..., min_length=2, max_length=3, description="비교할 도서 ID 리스트 (2~3개)")
    
    @field_validator('book_ids')
    @classmethod
    def validate_unique_ids(cls, v):
        """중복 ID 검증"""
        if len(v) != len(set(v)):
            raise ValueError("Duplicate book IDs are not allowed")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "book_ids": [1, 2, 3]
            }
        }
