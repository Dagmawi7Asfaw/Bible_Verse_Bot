"""
Verse history tracking service to prevent repetition within a year.
Ensures verses are not repeated within the same calendar year.
"""

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Set, Dict

from src.models.verse import BibleVerse
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VerseHistoryService:
    """Service for tracking and managing verse history to prevent repetition within a year."""
    
    def __init__(self, history_file: str = "data/verse_history.json"):
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.sent_verses_by_year: Dict[int, Set[str]] = {}
        self.available_verses: List[BibleVerse] = []
        self.load_history()
    
    def load_history(self):
        """Load verse history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    # Convert year keys back to integers
                    self.sent_verses_by_year = {
                        int(year): set(verses) 
                        for year, verses in data.get('sent_verses_by_year', {}).items()
                    }
                    logger.info(f"Loaded verse history for {len(self.sent_verses_by_year)} years")
            else:
                logger.info("No history file found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading verse history: {e}")
            self.sent_verses_by_year = {}
    
    def save_history(self):
        """Save verse history to file."""
        try:
            data = {
                'sent_verses_by_year': {
                    str(year): list(verses) 
                    for year, verses in self.sent_verses_by_year.items()
                },
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
    
    def get_current_year(self) -> int:
        """Get the current year."""
        return datetime.now().year
    
    def get_sent_verses_for_year(self, year: int) -> Set[str]:
        """Get verses sent in a specific year."""
        return self.sent_verses_by_year.get(year, set())
    
    def get_unused_verses_for_year(self, year: int) -> List[BibleVerse]:
        """Get verses that haven't been sent in the specified year."""
        sent_verses = self.get_sent_verses_for_year(year)
        unused = [verse for verse in self.available_verses 
                  if verse.reference not in sent_verses]
        logger.info(f"Found {len(unused)} unused verses for year {year} out of {len(self.available_verses)} total")
        return unused
    
    def mark_verse_sent(self, verse: BibleVerse, year: Optional[int] = None):
        """Mark a verse as sent for a specific year."""
        if year is None:
            year = self.get_current_year()
        
        if year not in self.sent_verses_by_year:
            self.sent_verses_by_year[year] = set()
        
        self.sent_verses_by_year[year].add(verse.reference)
        self.save_history()
        logger.info(f"Marked verse '{verse.reference}' as sent for year {year}")
    
    def reset_history_for_year(self, year: int):
        """Reset the verse history for a specific year."""
        if year in self.sent_verses_by_year:
            self.sent_verses_by_year[year].clear()
            self.save_history()
            logger.info(f"Verse history reset for year {year}")
    
    def reset_all_history(self):
        """Reset all verse history."""
        self.sent_verses_by_year.clear()
        self.save_history()
        logger.info("All verse history reset")
    
    def get_next_verse(self, year: Optional[int] = None) -> Optional[BibleVerse]:
        """Get the next available verse for the specified year, ensuring no repetition within that year."""
        if year is None:
            year = self.get_current_year()
        
        unused_verses = self.get_unused_verses_for_year(year)
        
        if not unused_verses:
            # All verses have been used this year, reset for this year and start over
            logger.info(f"All verses have been used for year {year}, resetting history for this year")
            self.reset_history_for_year(year)
            unused_verses = self.available_verses
        
        if unused_verses:
            # Select a random verse from unused ones
            import random
            selected_verse = random.choice(unused_verses)
            self.mark_verse_sent(selected_verse, year)
            return selected_verse
        
        return None
    
    def get_stats(self, year: Optional[int] = None) -> dict:
        """Get statistics about verse usage for a specific year or all years."""
        if year is None:
            year = self.get_current_year()
        
        total_verses = len(self.available_verses)
        used_verses = len(self.get_sent_verses_for_year(year))
        unused_verses = total_verses - used_verses
        
        return {
            'year': year,
            'total_verses': total_verses,
            'used_verses': used_verses,
            'unused_verses': unused_verses,
            'completion_percentage': (used_verses / total_verses * 100) if total_verses > 0 else 0
        }
    
    def get_all_years_stats(self) -> Dict[int, dict]:
        """Get statistics for all years in the history."""
        stats = {}
        for year in self.sent_verses_by_year.keys():
            stats[year] = self.get_stats(year)
        return stats
    
    def cleanup_old_years(self, keep_years: int = 2):
        """Clean up history for years older than the specified number of years to keep."""
        current_year = self.get_current_year()
        years_to_remove = []
        
        for year in self.sent_verses_by_year.keys():
            if year < (current_year - keep_years):
                years_to_remove.append(year)
        
        for year in years_to_remove:
            del self.sent_verses_by_year[year]
            logger.info(f"Removed history for year {year}")
        
        if years_to_remove:
            self.save_history()


# Global instance
verse_history = VerseHistoryService() 