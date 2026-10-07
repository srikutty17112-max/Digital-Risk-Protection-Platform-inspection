from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os
import tempfile


class Settings(BaseSettings):
    PROJECT_NAME: str = "BrandShield - Social Media Monitoring & Impersonation Detection"
    PROJECT_VERSION: str = "1.0.0"
    API_PORT: int = int(os.getenv("API_PORT", "8001"))

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(tempfile.gettempdir(), 'monitoring.db').replace(os.sep, '/')}"
        if (os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))
        else "sqlite:///./monitoring.db"
    )

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # Module 1 Integration
    MODULE1_API_BASE_URL: str = os.getenv("MODULE1_API_BASE_URL", "http://localhost:8000")
    MODULE1_API_KEY: str = os.getenv("MODULE1_API_KEY", "")

    # Module 3 Integration
    MODULE3_API_BASE_URL: str = os.getenv("MODULE3_API_BASE_URL", "http://localhost:8002")

    # Social Media API Keys
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET: str = os.getenv("TWITTER_API_SECRET", "")
    TWITTER_BEARER_TOKEN: str = os.getenv("TWITTER_BEARER_TOKEN", "")
    TWITTER_ACCESS_TOKEN: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_TOKEN_SECRET: str = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")

    LINKEDIN_CLIENT_ID: str = os.getenv("LINKEDIN_CLIENT_ID", "")
    LINKEDIN_CLIENT_SECRET: str = os.getenv("LINKEDIN_CLIENT_SECRET", "")
    LINKEDIN_ACCESS_TOKEN: str = os.getenv("LINKEDIN_ACCESS_TOKEN", "")

    INSTAGRAM_APP_ID: str = os.getenv("INSTAGRAM_APP_ID", "")
    INSTAGRAM_APP_SECRET: str = os.getenv("INSTAGRAM_APP_SECRET", "")
    INSTAGRAM_ACCESS_TOKEN: str = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")

    FACEBOOK_APP_ID: str = os.getenv("FACEBOOK_APP_ID", "")
    FACEBOOK_APP_SECRET: str = os.getenv("FACEBOOK_APP_SECRET", "")
    FACEBOOK_ACCESS_TOKEN: str = os.getenv("FACEBOOK_ACCESS_TOKEN", "")

    TIKTOK_CLIENT_KEY: str = os.getenv("TIKTOK_CLIENT_KEY", "")
    TIKTOK_CLIENT_SECRET: str = os.getenv("TIKTOK_CLIENT_SECRET", "")
    TIKTOK_ACCESS_TOKEN: str = os.getenv("TIKTOK_ACCESS_TOKEN", "")

    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")

    # AI/LLM
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Monitoring Settings
    SCAN_INTERVAL_MINUTES: int = int(os.getenv("SCAN_INTERVAL_MINUTES", "60"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.85"))
    MAX_CONCURRENT_SCANS: int = int(os.getenv("MAX_CONCURRENT_SCANS", "5"))
    DEFAULT_USER_ID: str = os.getenv("DEFAULT_USER_ID", "default_brand_owner_01")

    # Demo Mode
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def module1_configured(self) -> bool:
        return bool(self.MODULE1_API_BASE_URL)

    @property
    def twitter_configured(self) -> bool:
        return bool(self.TWITTER_BEARER_TOKEN or (self.TWITTER_API_KEY and self.TWITTER_API_SECRET))

    @property
    def linkedin_configured(self) -> bool:
        return bool(self.LINKEDIN_ACCESS_TOKEN or (self.LINKEDIN_CLIENT_ID and self.LINKEDIN_CLIENT_SECRET))

    @property
    def instagram_configured(self) -> bool:
        return bool(self.INSTAGRAM_ACCESS_TOKEN or (self.INSTAGRAM_APP_ID and self.INSTAGRAM_APP_SECRET))

    @property
    def facebook_configured(self) -> bool:
        return bool(self.FACEBOOK_ACCESS_TOKEN or (self.FACEBOOK_APP_ID and self.FACEBOOK_APP_SECRET))

    @property
    def gemini_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()