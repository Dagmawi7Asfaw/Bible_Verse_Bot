"""
Tests for the Bible API service.
"""

import pytest
import asyncio
from src.services.bible_api import BibleAPIService
from src.models.verse import VerseRequest


@pytest.mark.asyncio
async def test_get_random_verse():
    """Test getting a random verse."""
    async with BibleAPIService() as service:
        request = VerseRequest(random=True, translation="NIV")
        response = await service.get_verse(request)
        
        assert response.success is True
        assert response.verse is not None
        assert response.verse.reference is not None
        assert response.verse.text is not None
        assert response.verse.translation == "NIV"


@pytest.mark.asyncio
async def test_get_verse_by_reference():
    """Test getting a verse by reference."""
    async with BibleAPIService() as service:
        request = VerseRequest(reference="John 3:16", translation="NIV")
        response = await service.get_verse(request)
        
        assert response.success is True
        assert response.verse is not None
        assert "John" in response.verse.reference


@pytest.mark.asyncio
async def test_get_daily_verse():
    """Test getting a daily verse."""
    async with BibleAPIService() as service:
        response = await service.get_daily_verse()
        
        assert response.success is True
        assert response.verse is not None 