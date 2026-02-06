from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings - like Spring @ConfigurationProperties"""
    
    server_name: str = "my-mcp-server"
    log_level: str = "INFO"
    debug: bool = False
    
    # API keys / external config
    weather_api_key: Optional[str] = None
    database_url: str = "sqlite:///./data.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Singleton instance
settings = Settings()
