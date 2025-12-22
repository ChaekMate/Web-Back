from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 연결 확인
    echo=settings.DEBUG,  # SQL 쿼리 로깅 (개발 시)
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