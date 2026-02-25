"""
Configuration module for the Agent Demo backend.
Loads environment variables and provides configuration settings.
"""

import os
from dotenv import load_dotenv

# Force reload environment variables from .env file
load_dotenv(override=True)


class Settings:
    """Application settings loaded from environment variables."""

    @property
    def AZURE_OPENAI_API_KEY(self) -> str:
        return os.getenv("AZURE_OPENAI_API_KEY", "")
    
    @property
    def AZURE_OPENAI_ENDPOINT(self) -> str:
        return os.getenv("AZURE_OPENAI_ENDPOINT", "")
    
    @property
    def AZURE_OPENAI_DEPLOYMENT_NAME(self) -> str:
        return os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
    
    @property
    def AZURE_OPENAI_API_VERSION(self) -> str:
        return os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    CORS_ORIGINS: list = ["http://localhost:5173", "http://127.0.0.1:5173"]

    def validate(self) -> bool:
        """Validate that all required settings are configured."""
        required = [
            self.AZURE_OPENAI_API_KEY,
            self.AZURE_OPENAI_ENDPOINT,
            self.AZURE_OPENAI_DEPLOYMENT_NAME,
        ]
        return all(required)


settings = Settings()
