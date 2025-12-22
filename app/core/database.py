"""
데이터베이스 설정 및 세션 관리
SQLAlchemy + PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# 세션 로컬 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base 클래스 (모든 모델의 부모)
Base = declarative_base()


# 의존성 주입용 DB 세션
def get_db():
    """
    데이터베이스 세션 생성 및 종료
    FastAPI Depends에서 사용
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 데이터베이스 초기화 함수
def init_db():
    """
    데이터베이스 테이블 생성
    """
    # 모든 모델 import (테이블 생성을 위해)
    from app.models.user import User
    from app.models.book import Book
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
