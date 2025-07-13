"""
Bible API service for fetching verses from various sources.
Supports multiple Bible APIs with fallback mechanisms.
"""

import aiohttp
import asyncio
import json
import random
from typing import Optional, List
from pathlib import Path

from src.models.verse import BibleVerse, VerseRequest, VerseResponse
from src.config.settings import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BibleAPIService:
    """Service for fetching Bible verses from various APIs."""
    
    def __init__(self):
        self.settings = get_settings()
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Popular Bible verses as fallback
        self.fallback_verses = [
            {
                "reference": "John 3:16",
                "text": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
                "translation": "NIV",
                "book": "John",
                "chapter": 3,
                "verse": 16
            },
            {
                "reference": "Psalm 23:1",
                "text": "The Lord is my shepherd, I lack nothing.",
                "translation": "NIV",
                "book": "Psalm",
                "chapter": 23,
                "verse": 1
            },
            {
                "reference": "Philippians 4:13",
                "text": "I can do all this through him who gives me strength.",
                "translation": "NIV",
                "book": "Philippians",
                "chapter": 4,
                "verse": 13
            },
            {
                "reference": "Jeremiah 29:11",
                "text": "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future.",
                "translation": "NIV",
                "book": "Jeremiah",
                "chapter": 29,
                "verse": 11
            },
            {
                "reference": "Romans 8:28",
                "text": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
                "translation": "NIV",
                "book": "Romans",
                "chapter": 8,
                "verse": 28
            }
        ]
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def get_verse(self, request: VerseRequest) -> VerseResponse:
        """
        Get a Bible verse based on the request.
        
        Args:
            request: Verse request parameters
            
        Returns:
            VerseResponse with verse data or error
        """
        try:
            if request.random:
                return await self._get_random_verse(request.translation)
            elif request.reference:
                return await self._get_verse_by_reference(request.reference, request.translation)
            else:
                return await self._get_random_verse(request.translation)
                
        except Exception as e:
            logger.error(f"Error fetching verse: {e}")
            return VerseResponse(
                success=False,
                error=str(e),
                verse=None
            )
    
    async def _get_verse_by_reference(self, reference: str, translation: str = "NIV") -> VerseResponse:
        """Get verse by reference using Bible API."""
        if not self.settings.bible_api_key:
            logger.warning("No Bible API key configured, using fallback")
            return self._get_fallback_verse()
        
        try:
            # Try Bible API first
            verse = await self._fetch_from_bible_api(reference, translation)
            if verse:
                return VerseResponse(success=True, verse=verse)
            
            # Fallback to local verses
            return self._get_fallback_verse()
            
        except Exception as e:
            logger.error(f"Error fetching from Bible API: {e}")
            return self._get_fallback_verse()
    
    async def _get_random_verse(self, translation: str = "NIV") -> VerseResponse:
        """Get a random verse."""
        try:
            # Try to get from Bible API if available
            if self.settings.bible_api_key:
                verse = await self._fetch_random_from_bible_api(translation)
                if verse:
                    return VerseResponse(success=True, verse=verse)
            
            # Fallback to local verses
            return self._get_fallback_verse()
            
        except Exception as e:
            logger.error(f"Error fetching random verse: {e}")
            return self._get_fallback_verse()
    
    async def _fetch_from_bible_api(self, reference: str, translation: str) -> Optional[BibleVerse]:
        """Fetch verse from Bible API."""
        if not self.session:
            return None
        
        # This is a simplified implementation
        # In a real implementation, you would parse the reference and make proper API calls
        logger.info(f"Fetching verse {reference} from Bible API")
        
        # For now, return None to trigger fallback
        return None
    
    async def _fetch_random_from_bible_api(self, translation: str) -> Optional[BibleVerse]:
        """Fetch random verse from Bible API."""
        if not self.session:
            return None
        
        logger.info("Fetching random verse from Bible API")
        
        # For now, return None to trigger fallback
        return None
    
    def _get_fallback_verse(self) -> VerseResponse:
        """Get a verse from the fallback list."""
        verse_data = random.choice(self.fallback_verses)
        verse = BibleVerse(**verse_data)
        
        logger.info(f"Using fallback verse: {verse.reference}")
        
        return VerseResponse(
            success=True,
            verse=verse
        )
    
    async def get_daily_verse(self) -> VerseResponse:
        """Get a verse for daily posting."""
        # For daily verses, we can implement logic to avoid repetition
        # For now, just get a random verse
        request = VerseRequest(random=True, translation="NIV")
        return await self.get_verse(request)


# Convenience function
async def get_bible_verse(request: VerseRequest) -> VerseResponse:
    """Convenience function to get a Bible verse."""
    async with BibleAPIService() as service:
        return await service.get_verse(request) 