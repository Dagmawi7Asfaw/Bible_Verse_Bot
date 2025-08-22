"""
Configuration settings for the Bible Verse Telegram Bot.
Uses Pydantic for type safety and validation.
"""

import os
from typing import Optional
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseModel):
    """Application settings with validation."""
    
    # Telegram Configuration
    telegram_bot_token: str
    telegram_chat_id: str
    telegram_chat_ids: list[str] = []
    
    # Bot Settings
    verse_schedule_time: str = "09:00"
    verse_schedule_timezone: str = "UTC"
    verse_schedule_times: list[str] = []
    log_level: str = "INFO"
    
    # Database/Storage
    database_url: Optional[str] = None
    
    @field_validator('verse_schedule_time')
    @classmethod
    def validate_schedule_time(cls, v):
        """Validate time format HH:MM."""
        try:
            hour, minute = map(int, v.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except (ValueError, AttributeError):
            raise ValueError('Time must be in HH:MM format')
        return v
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of: {valid_levels}')
        return v.upper()
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get the global settings instance."""
    # Load environment variables
    load_dotenv()
    
    # Parse multiple chat IDs
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
    chat_ids_str = os.getenv('TELEGRAM_CHAT_IDS', '')
    
    # Combine single chat ID with multiple chat IDs
    all_chat_ids = []
    if chat_id:
        all_chat_ids.append(chat_id)
    if chat_ids_str:
        # Split by comma and clean up whitespace
        additional_ids = [cid.strip() for cid in chat_ids_str.split(',') if cid.strip()]
        all_chat_ids.extend(additional_ids)
    
    # Parse multiple schedule times
    schedule_times_str = os.getenv('VERSE_SCHEDULE_TIMES', '')
    schedule_time = os.getenv('VERSE_SCHEDULE_TIME', '09:00')
    all_schedule_times = []
    if schedule_times_str:
        all_schedule_times = [t.strip() for t in schedule_times_str.split(',') if t.strip()]
    elif schedule_time:
        all_schedule_times = [schedule_time]
    
    # Create settings from environment
    return Settings(
        telegram_bot_token=os.getenv('TELEGRAM_BOT_TOKEN', ''),
        telegram_chat_id=os.getenv('TELEGRAM_CHAT_ID', ''),
        telegram_chat_ids=all_chat_ids,
        verse_schedule_time=schedule_time,
        verse_schedule_timezone=os.getenv('VERSE_SCHEDULE_TIMEZONE', 'UTC'),
        verse_schedule_times=all_schedule_times,
        log_level=os.getenv('LOG_LEVEL', 'INFO'),
        database_url=os.getenv('DATABASE_URL')
    )


# Global settings instance
settings = get_settings() 