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
from src.services.verse_history import verse_history

logger = get_logger(__name__)


class BibleAPIService:
    """Service for fetching Bible verses from various APIs."""
    
    def __init__(self):
        self.settings = get_settings()
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Bible API endpoints
        self.bible_api_base = "https://cdn.jsdelivr.net/gh/wldeh/bible-api"
        self.available_bibles = [
            "en-kjv",    # King James Version
            "en-asv",    # American Standard Version
            "en-bbe",    # Bible in Basic English
            "en-dby",    # Darby Bible
            "en-wbt",    # Webster's Bible
            "en-web",    # World English Bible
            "en-ylt"     # Young's Literal Translation
        ]
        
        # Bible books with their chapter counts for randomization
        self.bible_books = {
            "genesis": 50, "exodus": 40, "leviticus": 27, "numbers": 36, "deuteronomy": 34,
            "joshua": 24, "judges": 21, "ruth": 4, "1samuel": 31, "2samuel": 24,
            "1kings": 22, "2kings": 25, "1chronicles": 29, "2chronicles": 36, "ezra": 10,
            "nehemiah": 13, "esther": 10, "job": 42, "psalms": 150, "proverbs": 31,
            "ecclesiastes": 12, "songofsolomon": 8, "isaiah": 66, "jeremiah": 52,
            "lamentations": 5, "ezekiel": 48, "daniel": 12, "hosea": 14, "joel": 3,
            "amos": 9, "obadiah": 1, "jonah": 4, "micah": 7, "nahum": 3,
            "habakkuk": 3, "zephaniah": 3, "haggai": 2, "zechariah": 14, "malachi": 4,
            "matthew": 28, "mark": 16, "luke": 24, "john": 21, "acts": 28,
            "romans": 16, "1corinthians": 16, "2corinthians": 13, "galatians": 6,
            "ephesians": 6, "philippians": 4, "colossians": 4, "1thessalonians": 5,
            "2thessalonians": 3, "1timothy": 6, "2timothy": 4, "titus": 3,
            "philemon": 1, "hebrews": 13, "james": 5, "1peter": 5, "2peter": 3,
            "1john": 5, "2john": 1, "3john": 1, "jude": 1, "revelation": 22
        }
        
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
            },
            {
                "reference": "Proverbs 3:5-6",
                "text": "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.",
                "translation": "NIV",
                "book": "Proverbs",
                "chapter": 3,
                "verse": 5
            },
            {
                "reference": "Isaiah 40:31",
                "text": "But those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.",
                "translation": "NIV",
                "book": "Isaiah",
                "chapter": 40,
                "verse": 31
            },
            {
                "reference": "Matthew 28:19-20",
                "text": "Therefore go and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit, and teaching them to obey everything I have commanded you. And surely I am with you always, to the very end of the age.",
                "translation": "NIV",
                "book": "Matthew",
                "chapter": 28,
                "verse": 19
            },
            {
                "reference": "Galatians 5:22-23",
                "text": "But the fruit of the Spirit is love, joy, peace, forbearance, kindness, goodness, faithfulness, gentleness and self-control. Against such things there is no law.",
                "translation": "NIV",
                "book": "Galatians",
                "chapter": 5,
                "verse": 22
            },
            {
                "reference": "Joshua 1:9",
                "text": "Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.",
                "translation": "NIV",
                "book": "Joshua",
                "chapter": 1,
                "verse": 9
            }
        ]
        
        # Initialize verse history with fallback verses
        fallback_verse_objects = [BibleVerse(**verse_data) for verse_data in self.fallback_verses]
        verse_history.set_available_verses(fallback_verse_objects)
    
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
        """Get a truly random verse from the Bible API."""
        if not self.session:
            return self._get_fallback_verse()
        
        try:
            # Map translation to available Bible version
            bible_version = self._map_translation_to_version(translation)
            
            # Try up to 5 random attempts to get a working verse
            for attempt in range(5):
                try:
                    # Pick a random book
                    book = random.choice(list(self.bible_books.keys()))
                    max_chapters = self.bible_books[book]
                    
                    # Pick a random chapter (avoid chapter 1 for variety)
                    chapter = random.randint(2, max_chapters) if max_chapters > 1 else 1
                    
                    # For books with many chapters, try to get a verse from the middle
                    if max_chapters > 20:
                        # Estimate verses per chapter (roughly 20-30 for most books)
                        estimated_verses = random.randint(15, 35)
                        verse_num = random.randint(1, min(estimated_verses, 50))
                    else:
                        # For shorter books, use a reasonable verse range
                        verse_num = random.randint(1, 30)
                    
                    # Construct reference
                    reference = f"{self._format_book_name(book)} {chapter}:{verse_num}"
                    
                    logger.info(f"Attempting random verse: {reference} (attempt {attempt + 1})")
                    
                    # Try to fetch this verse
                    verse = await self._fetch_from_bible_api(reference, translation)
                    if verse:
                        logger.info(f"Successfully fetched random verse: {reference}")
                        return VerseResponse(success=True, verse=verse)
                        
                except Exception as e:
                    logger.debug(f"Attempt {attempt + 1} failed: {e}")
                    continue
            
            logger.warning("Failed to fetch random verse after 5 attempts, using fallback")
            return self._get_fallback_verse()
                    
        except Exception as e:
            logger.error(f"Error fetching random verse from Bible API: {e}")
            return self._get_fallback_verse()
    
    def _format_book_name(self, book: str) -> str:
        """Format book name for display (e.g., '1corinthians' -> '1 Corinthians')."""
        if book.startswith('1') or book.startswith('2') or book.startswith('3'):
            # Handle numbered books
            number = book[0]
            name = book[1:].title()
            return f"{number} {name}"
        elif book == "songofsolomon":
            return "Song of Solomon"
        else:
            return book.title()
    
    async def _fetch_from_bible_api(self, reference: str, translation: str = "NIV") -> Optional[BibleVerse]:
        """Fetch verse from Bible API using wldeh/bible-api."""
        if not self.session:
            return None
        
        try:
            # Parse reference (e.g., "John 3:16" -> book="john", chapter=3, verse=16)
            parsed = self._parse_reference(reference)
            if not parsed:
                logger.warning(f"Could not parse reference: {reference}")
                return None
            
            book, chapter, verse_num = parsed
            
            # Map translation to available Bible version
            bible_version = self._map_translation_to_version(translation)
            
            # Construct API URL
            url = f"{self.bible_api_base}/bibles/{bible_version}/books/{book}/chapters/{chapter}/verses/{verse_num}.json"
            
            logger.info(f"Fetching verse from: {url}")
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Create BibleVerse object
                    verse = BibleVerse(
                        reference=reference,
                        text=data.get("text", ""),
                        translation=bible_version.upper(),
                        book=book.title(),
                        chapter=chapter,
                        verse=verse_num
                    )
                    
                    logger.info(f"Successfully fetched verse: {reference}")
                    return verse
                else:
                    logger.warning(f"API returned status {response.status} for {url}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching verse from Bible API: {e}")
            return None
    
    def _parse_reference(self, reference: str) -> Optional[tuple]:
        """Parse Bible reference into book, chapter, and verse."""
        try:
            # Remove any extra spaces and split
            parts = reference.strip().split()
            
            if len(parts) < 2:
                return None
            
            # Handle books with multiple words (e.g., "Song of Solomon")
            if len(parts) >= 4 and parts[0].lower() in ["song", "1", "2", "3"]:
                # Handle "Song of Solomon" or numbered books
                if parts[0].lower() in ["1", "2", "3"]:
                    book = f"{parts[0]}{parts[1].title()}"
                    chapter_verse = parts[2]
                else:
                    book = f"{parts[0].title()} {parts[1]} {parts[2].title()}"
                    chapter_verse = parts[3]
            elif len(parts) >= 3 and parts[1].lower() in ["of", "the"]:
                # Handle "Book of Name" format
                book = f"{parts[0].title()} {parts[1]} {parts[2].title()}"
                chapter_verse = parts[3] if len(parts) > 3 else "1:1"
            else:
                # Simple format like "John 3:16"
                book = parts[0].title()
                chapter_verse = parts[1]
            
            # Parse chapter:verse
            if ":" in chapter_verse:
                chapter, verse = chapter_verse.split(":")
                chapter = int(chapter)
                verse = int(verse)
            else:
                # Just chapter, use verse 1
                chapter = int(chapter_verse)
                verse = 1
            
            # Normalize book name for API
            book = self._normalize_book_name(book)
            
            return (book, chapter, verse)
            
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing reference '{reference}': {e}")
            return None
    
    def _normalize_book_name(self, book: str) -> str:
        """Normalize book names for the API."""
        # Convert to lowercase and remove spaces for API compatibility
        book = book.lower().replace(" ", "")
        
        # Handle special cases
        book_mappings = {
            "1corinthians": "1corinthians",
            "2corinthians": "2corinthians",
            "1thessalonians": "1thessalonians",
            "2thessalonians": "2thessalonians",
            "1timothy": "1timothy",
            "2timothy": "2timothy",
            "1peter": "1peter",
            "2peter": "2peter",
            "1john": "1john",
            "2john": "2john",
            "3john": "3john",
            "songofsolomon": "songofsolomon",
            "revelation": "revelation"
        }
        
        return book_mappings.get(book, book)
    
    def _map_translation_to_version(self, translation: str) -> str:
        """Map translation names to available Bible versions."""
        translation = translation.upper()
        
        # Map common translation names to available versions
        translation_mappings = {
            "NIV": "en-kjv",      # NIV not available, use KJV
            "KJV": "en-kjv",
            "ASV": "en-asv",
            "BBE": "en-bbe",
            "DBY": "en-dby",
            "WBT": "en-wbt",
            "WEB": "en-web",
            "YLT": "en-ylt"
        }
        
        return translation_mappings.get(translation, "en-kjv")  # Default to KJV
    
    def _get_fallback_verse(self) -> VerseResponse:
        """Get a verse from the fallback list using history tracking."""
        verse = verse_history.get_next_verse()
        
        if verse:
            logger.info(f"Using non-repeating verse: {verse.reference}")
            return VerseResponse(
                success=True,
                verse=verse
            )
        else:
            # Fallback to random selection if history service fails
            verse_data = random.choice(self.fallback_verses)
            verse = BibleVerse(**verse_data)
            logger.warning(f"History service failed, using random verse: {verse.reference}")
            return VerseResponse(
                success=True,
                verse=verse
            )
    
    async def get_daily_verse(self) -> VerseResponse:
        """Get a verse for daily posting with rotation and variety."""
        try:
            # Rotate through different translations for variety
            translations = ["KJV", "ASV", "BBE", "DBY", "WBT", "WEB", "YLT"]
            
            # Use date-based rotation to ensure variety
            import datetime
            today = datetime.date.today()
            day_of_year = today.timetuple().tm_yday
            
            # Rotate translation every week
            translation_index = (day_of_year // 7) % len(translations)
            selected_translation = translations[translation_index]
            
            logger.info(f"Using translation: {selected_translation} for day {day_of_year}")
            
            # Get a random verse with the selected translation
            request = VerseRequest(random=True, translation=selected_translation)
            return await self.get_verse(request)
            
        except Exception as e:
            logger.error(f"Error in get_daily_verse: {e}")
            # Fallback to KJV if rotation fails
            request = VerseRequest(random=True, translation="KJV")
            return await self.get_verse(request)


# Convenience function
async def get_bible_verse(request: VerseRequest) -> VerseResponse:
    """Convenience function to get a Bible verse."""
    async with BibleAPIService() as service:
        return await service.get_verse(request) 