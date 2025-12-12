"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Reportify - Medical Report Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    MONGODB_URL: str = "<mongodb-connection>"
    DATABASE_NAME: str = "RedCliffe_Labs"
    COLLECTION_NAME: str = "patient_details"
    
    # AI/LLM
    GEMINI_API_KEY: str = "<api-key>"
    OPENAI_API_KEY: Optional[str] = None
    
    # Paths
    STATIC_DIR: str = "static"
    TEMPLATES_DIR: str = "templates"
    RESOURCES_DIR: str = "resources"
    OUTPUT_DIR: str = "outputs/generated_pdfs"
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
