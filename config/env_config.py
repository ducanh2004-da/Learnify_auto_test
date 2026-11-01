from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE_PATH, override=False)


class Settings(BaseSettings):
    """
    Application & Test Configuration powered by pydantic-settings.
    Provides safe default values so CI/CD (GitHub Actions) will not crash
    with a ValidationError when the gitignored .env file is absent.
    """
    ENV: str = Field(default="dev", description="Target environment: dev | staging | prod")
    BASE_URL: str = Field(default="https://learnify.io.vn", description="Frontend Base URL")
    API_URL: str = Field(default="https://learnify-be.onrender.com/graphql", description="GraphQL API URL")
    DB_URL: Optional[str] = Field(default="", description="Database connection string (optional)")

    # Admin credentials for test data cleanup (loaded securely from .env or CI secrets)
    ADMIN_EMAIL: str = Field(default="", description="Admin email for user cleanup")
    ADMIN_PASSWORD: str = Field(default="", description="Admin password for user cleanup")

    # Playwright execution settings
    HEADLESS: bool = Field(default=True, description="Run browser in headless mode")
    DEFAULT_TIMEOUT: int = Field(default=30000, description="Default Playwright timeout in ms")

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()


class EnvConfig:
    """
    Backward-compatible configuration wrapper used across Page Objects,
    Workflows, and Pytest fixtures.
    """
    def __init__(self, env: Optional[str] = None):
        self.env = (env or settings.ENV).lower()
        self.config = self.load_config()

    def load_config(self) -> dict:
        if self.env == "staging":
            return {
                "base_url": settings.BASE_URL.rstrip("/") if "staging" in settings.BASE_URL else "https://staging.example.com",
                "api_url": settings.API_URL if "staging" in settings.API_URL else "https://staging.example.com/api",
                "db_url": settings.DB_URL or "",
                "admin_email": settings.ADMIN_EMAIL,
                "admin_password": settings.ADMIN_PASSWORD,
                "headless": settings.HEADLESS,
                "default_timeout": settings.DEFAULT_TIMEOUT,
            }

        # Default to "dev" environment settings (overridable via .env or GitHub Secrets/Vars)
        return {
            "base_url": settings.BASE_URL.rstrip("/"),
            "api_url": settings.API_URL,
            "db_url": settings.DB_URL or "",
            "admin_email": settings.ADMIN_EMAIL,
            "admin_password": settings.ADMIN_PASSWORD,
            "headless": settings.HEADLESS,
            "default_timeout": settings.DEFAULT_TIMEOUT,
        }
