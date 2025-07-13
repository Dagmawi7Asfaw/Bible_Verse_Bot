"""
Data models for Bible verses and related entities.
Uses Pydantic for validation and serialization.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class BibleVerse(BaseModel):
    """Model representing a Bible verse."""
    
    reference: str = Field(..., description="Verse reference (e.g., 'John 3:16')")
    text: str = Field(..., description="Verse text content")
    translation: str = Field(..., description="Bible translation (e.g., 'NIV', 'KJV')")
    book: str = Field(..., description="Book name")
    chapter: int = Field(..., description="Chapter number")
    verse: int = Field(..., description="Verse number")
    
    # Optional fields
    context: Optional[str] = Field(None, description="Additional context or commentary")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")
    source: Optional[str] = Field(None, description="Source API or database")
    
    class Config:
        schema_extra = {
            "example": {
                "reference": "John 3:16",
                "text": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
                "translation": "NIV",
                "book": "John",
                "chapter": 3,
                "verse": 16,
                "context": "Jesus speaking to Nicodemus about salvation",
                "tags": ["salvation", "love", "eternal life"],
                "source": "bible_api"
            }
        }


class VerseRequest(BaseModel):
    """Model for verse requests."""
    
    reference: Optional[str] = Field(None, description="Specific verse reference")
    book: Optional[str] = Field(None, description="Book name")
    chapter: Optional[int] = Field(None, description="Chapter number")
    verse: Optional[int] = Field(None, description="Verse number")
    translation: str = Field(default="NIV", description="Preferred translation")
    random: bool = Field(default=False, description="Request random verse")
    
    class Config:
        schema_extra = {
            "example": {
                "reference": "John 3:16",
                "translation": "NIV",
                "random": False
            }
        }


class VerseResponse(BaseModel):
    """Model for verse API responses."""
    
    success: bool = Field(..., description="Whether the request was successful")
    verse: Optional[BibleVerse] = Field(None, description="Bible verse data")
    error: Optional[str] = Field(None, description="Error message if request failed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "verse": {
                    "reference": "John 3:16",
                    "text": "For God so loved the world...",
                    "translation": "NIV",
                    "book": "John",
                    "chapter": 3,
                    "verse": 16
                },
                "timestamp": "2024-01-01T09:00:00"
            }
        }


class DailyVerse(BaseModel):
    """Model for daily verse scheduling."""
    
    date: datetime = Field(..., description="Date for the verse")
    verse: BibleVerse = Field(..., description="Verse for the day")
    sent: bool = Field(default=False, description="Whether verse was sent")
    sent_at: Optional[datetime] = Field(None, description="When verse was sent")
    
    class Config:
        schema_extra = {
            "example": {
                "date": "2024-01-01T00:00:00",
                "verse": {
                    "reference": "John 3:16",
                    "text": "For God so loved the world...",
                    "translation": "NIV",
                    "book": "John",
                    "chapter": 3,
                    "verse": 16
                },
                "sent": False
            }
        } 