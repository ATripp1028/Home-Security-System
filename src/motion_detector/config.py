"""Configuration management for the motion detector."""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


class Config:
    """Configuration settings for the motion detector."""

    # Camera settings
    CAMERA_INDEX: int = int(os.getenv("CAMERA_INDEX", "0"))
    MOTION_THRESHOLD: float = float(os.getenv("MOTION_THRESHOLD", "1000.0"))
    MIN_CONTOUR_AREA: int = int(os.getenv("MIN_CONTOUR_AREA", "500"))

    # Notification settings
    NOTIFICATION_ENABLED: bool = os.getenv("NOTIFICATION_ENABLED", "true").lower() == "true"
    
    # Email settings
    EMAIL_ENABLED: bool = os.getenv("EMAIL_ENABLED", "true").lower() == "true"
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "alexhtripp@gmail.com")
    EMAIL_TO: str = os.getenv("EMAIL_TO", "aht23490@ucmo.edu")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "txqb ktqk wlfs afqi")

    # Cooldown settings (prevent spam)
    NOTIFICATION_COOLDOWN_SECONDS: int = int(os.getenv("NOTIFICATION_COOLDOWN_SECONDS", "60"))

    @classmethod
    def validate(cls) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        if cls.EMAIL_ENABLED and cls.NOTIFICATION_ENABLED:
            if not cls.EMAIL_FROM:
                errors.append("EMAIL_FROM is required when email notifications are enabled")
            if not cls.EMAIL_TO:
                errors.append("EMAIL_TO is required when email notifications are enabled")
            if not cls.EMAIL_PASSWORD:
                errors.append("EMAIL_PASSWORD is required when email notifications are enabled")
        
        return errors
