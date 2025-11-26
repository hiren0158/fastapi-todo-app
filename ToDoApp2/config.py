"""
Configuration management for the FastAPI application.
Uses Pydantic Settings for environment variable management.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "FastAPI Todo Application"
    debug: bool = False
    
    # MongoDB
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_db_name: str = os.getenv("MONGODB_DB_NAME", "todoapp")
    
    # Security
    secret_key: str = os.getenv('SECRET_KEY', 'change-me-in-production-use-a-secure-random-key')
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 20
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8081
    timezone: str = "UTC"

    # Daily lifecycle + notifications
    daily_reset_enabled: bool = True
    summary_email_enabled: bool = False
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True
    email_from: Optional[str] = None
    sender_email: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
