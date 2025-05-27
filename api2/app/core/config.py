from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Stock Analysis API"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"  # Change this in production
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
    ]
    
    # Database
    DATABASE_URL: str = str(Path(__file__).parent.parent.parent.parent / "api 1" / "stock_analysis.db")
    STOCK_ANALYSIS_DB: str = str(Path(__file__).parent.parent.parent.parent / "api 1" / "stock_analysis.db")
    
    # Rate Limiting
    DEFAULT_REQUESTS_PER_SECOND: int = 10
    DEFAULT_REQUESTS_PER_MONTH: int = 10000
    
    # Plan Configuration
    DEFAULT_PLAN_DURATION: int = 30  # días
    MIN_REQUESTS_PER_SECOND: int = 1
    MAX_REQUESTS_PER_SECOND: int = 100
    MIN_REQUESTS_PER_MONTH: int = 1000
    MAX_REQUESTS_PER_MONTH: int = 1000000
    
    class Config:
        case_sensitive = True

settings = Settings() 