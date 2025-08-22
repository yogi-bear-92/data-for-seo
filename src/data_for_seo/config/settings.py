"""Settings and configuration for Data for SEO."""

import os
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application settings
    app_name: str = Field(default="Data for SEO", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment")
    
    # API settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_workers: int = Field(default=1, description="Number of API workers")
    
    # Data for SEO API settings
    dataforseo_api_url: HttpUrl = Field(
        default="https://api.dataforseo.com/v3",
        description="Data for SEO API base URL"
    )
    dataforseo_username: Optional[str] = Field(
        default=None, description="Data for SEO API username"
    )
    dataforseo_password: Optional[str] = Field(
        default=None, description="Data for SEO API password"
    )
    dataforseo_rate_limit: int = Field(
        default=100, description="API rate limit per minute"
    )
    
    # Redis settings
    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )
    redis_password: Optional[str] = Field(
        default=None, description="Redis password"
    )
    redis_db: int = Field(default=0, description="Redis database number")
    
    # ChromaDB settings
    chroma_host: str = Field(default="localhost", description="ChromaDB host")
    chroma_port: int = Field(default=8000, description="ChromaDB port")
    chroma_persist_directory: str = Field(
        default="./data/chroma", description="ChromaDB persistence directory"
    )
    chroma_collection_name: str = Field(
        default="seo_knowledge", description="ChromaDB collection name"
    )
    
    # Embedding model settings
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Sentence transformer model for embeddings"
    )
    embedding_dimension: int = Field(
        default=384, description="Embedding vector dimension"
    )
    
    # Task processing settings
    max_concurrent_tasks: int = Field(
        default=10, description="Maximum concurrent tasks"
    )
    task_timeout: int = Field(
        default=300, description="Task timeout in seconds"
    )
    retry_attempts: int = Field(
        default=3, description="Number of retry attempts"
    )
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    log_file: Optional[str] = Field(
        default=None, description="Log file path"
    )
    
    # Security settings
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for encryption"
    )
    allowed_hosts: List[str] = Field(
        default_factory=lambda: ["*"], description="Allowed hosts"
    )
    cors_origins: List[str] = Field(
        default_factory=lambda: ["*"], description="CORS allowed origins"
    )
    
    # Agent settings
    agent_heartbeat_interval: int = Field(
        default=30, description="Agent heartbeat interval in seconds"
    )
    agent_timeout: int = Field(
        default=120, description="Agent timeout in seconds"
    )
    
    # SEO-specific settings
    default_search_engine: str = Field(
        default="google", description="Default search engine"
    )
    default_location: str = Field(
        default="United States", description="Default location"
    )
    default_language: str = Field(
        default="en", description="Default language"
    )
    
    # Data retention settings
    keyword_data_retention_days: int = Field(
        default=365, description="Keyword data retention in days"
    )
    ranking_data_retention_days: int = Field(
        default=730, description="Ranking data retention in days"
    )
    audit_data_retention_days: int = Field(
        default=90, description="Audit data retention in days"
    )
    
    # Performance settings
    batch_size: int = Field(
        default=100, description="Default batch size for processing"
    )
    cache_ttl: int = Field(
        default=3600, description="Cache TTL in seconds"
    )
    
    # External service settings
    user_agent: str = Field(
        default="DataForSEO-Agent/1.0", description="User agent for web requests"
    )
    request_timeout: int = Field(
        default=30, description="HTTP request timeout in seconds"
    )
    max_retries: int = Field(
        default=3, description="Maximum HTTP request retries"
    )
    
    @property
    def dataforseo_auth(self) -> Optional[tuple[str, str]]:
        """Get Data for SEO API authentication tuple."""
        if self.dataforseo_username and self.dataforseo_password:
            return (self.dataforseo_username, self.dataforseo_password)
        return None
    
    @property
    def chroma_url(self) -> str:
        """Get ChromaDB URL."""
        return f"http://{self.chroma_host}:{self.chroma_port}"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment.lower() == "development"
    
    def get_log_config(self) -> dict:
        """Get logging configuration."""
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.log_format,
                },
                "structured": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": self.log_level,
                },
            },
            "root": {
                "level": self.log_level,
                "handlers": ["console"],
            },
            "loggers": {
                "data_for_seo": {
                    "level": self.log_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }
        
        # Add file handler if log file is specified
        if self.log_file:
            config["handlers"]["file"] = {
                "class": "logging.FileHandler",
                "filename": self.log_file,
                "formatter": "structured",
                "level": self.log_level,
            }
            config["root"]["handlers"].append("file")
            config["loggers"]["data_for_seo"]["handlers"].append("file")
        
        return config


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
