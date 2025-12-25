from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 프로젝트 기본 정보
    PROJECT_NAME: str = "ChaekMate API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # 서버 설정
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000"
    
    # 데이터베이스
    DATABASE_URL: str
    
    # Redis (향후 사용)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT 인증
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OpenAI API (향후 사용)
    OPENAI_API_KEY: str = ""
    
    # Anthropic Claude API (향후 사용)
    ANTHROPIC_API_KEY: str = ""
    
    # Naver Book Search API
    NAVER_CLIENT_ID: str = ""
    NAVER_CLIENT_SECRET: str = ""
    
    # 파일 업로드
    MAX_FILE_SIZE: int = 10485760
    UPLOAD_DIR: str = "uploads/"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """CORS origins를 리스트로 변환"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# 설정 인스턴스 생성
settings = Settings()
