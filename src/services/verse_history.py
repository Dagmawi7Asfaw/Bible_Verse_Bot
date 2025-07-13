"""
Verse history tracking service to prevent repetition.
Ensures all verses are used before any can be repeated.
"""

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Set

from src.models.verse import BibleVerse
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VerseHistoryService:
    """Service for tracking and managing verse history to prevent repetition."""
    
    def __init__(self, history_file: str = "data/verse_history.json"):
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.sent_verses: Set[str] = set()
        self.available_verses: List[BibleVerse] = []
        self.load_history()
    
    def load_history(self):
        """Load verse history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.sent_verses = set(data.get('sent_verses', []))
                    logger.info(f"Loaded {len(self.sent_verses)} sent verses from history")
            else:
                logger.info("No history file found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading verse history: {e}")
            self.sent_verses = set()
    
    def save_history(self):
        """Save verse history to file."""
        try:
            data = {
                'sent_verses': list(self.sent_verses),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug("Verse history saved")
        except Exception as e:
            logger.error(f"Error saving verse history: {e}")
    
    def set_available_verses(self, verses: List[BibleVerse]):
        """Set the list of available verses."""
        self.available_verses = verses
        logger.info(f"Set {len(verses)} available verses")
    
    def get_unused_verses(self) -> List[BibleVerse]:
        """Get verses that haven't been sent yet."""
        unused = [verse for verse in self.available_verses 
                  if verse.reference not in self.sent_verses]
        logger.info(f"Found {len(unused)} unused verses out of {len(self.available_verses)} total")
        return unused
    
    def mark_verse_sent(self, verse: BibleVerse):
        """Mark a verse as sent."""
        self.sent_verses.add(verse.reference)
        self.save_history()
        logger.info(f"Marked verse '{verse.reference}' as sent")
    
    def reset_history(self):
        """Reset the verse history (use all verses again)."""
        self.sent_verses.clear()
        self.save_history()
        logger.info("Verse history reset - all verses available again")
    
    def get_next_verse(self) -> Optional[BibleVerse]:
        """Get the next available verse, ensuring no repetition."""
        unused_verses = self.get_unused_verses()
        
        if not unused_verses:
            # All verses have been used, reset and start over
            logger.info("All verses have been used, resetting history")
            self.reset_history()
            unused_verses = self.available_verses
        
        if unused_verses:
            # Select a random verse from unused ones
            import random
            selected_verse = random.choice(unused_verses)
            self.mark_verse_sent(selected_verse)
            return selected_verse
        
        return None
    
    def get_stats(self) -> dict:
        """Get statistics about verse usage."""
        total_verses = len(self.available_verses)
        used_verses = len(self.sent_verses)
        unused_verses = total_verses - used_verses
        
        return {
            'total_verses': total_verses,
            'used_verses': used_verses,
            'unused_verses': unused_verses,
            'completion_percentage': (used_verses / total_verses * 100) if total_verses > 0 else 0
        }
    
    def cleanup_old_history(self, days: int = 30):
        """Clean up history older than specified days."""
        try:
            if self.history_file.exists():
                file_age = datetime.now() - datetime.fromtimestamp(self.history_file.stat().st_mtime)
                if file_age.days > days:
                    logger.info(f"History file is {file_age.days} days old, cleaning up")
                    self.reset_history()
        except Exception as e:
            logger.error(f"Error cleaning up history: {e}")


# Global instance
verse_history = VerseHistoryService() 