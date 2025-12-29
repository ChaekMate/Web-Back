"""
ChaekMate Backend API
FastAPI 애플리케이션 메인 엔트리포인트
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db

# 라우터 import
from app.api.v1 import auth
from app.api.v1 import auth, books
from app.api.v1 import auth, books, recommendations

# FastAPI 앱 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI 기반 도서 추천 및 비교 플랫폼",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행"""
    init_db()
    print("✅ 데이터베이스 초기화 완료")


@app.get("/")
async def root():
    """헬스 체크 엔드포인트"""
    return {
        "message": "ChaekMate API Server",
        "status": "running",
        "version": settings.VERSION
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}


# 라우터 등록
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["인증"])
app.include_router(books.router, prefix=f"{settings.API_V1_PREFIX}/books", tags=["도서"])
app.include_router(recommendations.router, prefix=f"{settings.API_V1_PREFIX}/recommendations", tags=["AI 추천"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
