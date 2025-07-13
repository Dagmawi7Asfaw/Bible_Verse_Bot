#!/usr/bin/env python3
"""
Script to view and manage verse history statistics.
Shows which verses have been sent and which are still available for each year.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.verse_history import verse_history
from src.services.bible_api import BibleAPIService
from src.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger()
logger = get_logger(__name__)


def load_available_verses():
    """Load available verses into the verse history service."""
    try:
        # Initialize Bible API service which sets available verses
        bible_service = BibleAPIService()
        logger.info("Loaded available verses into verse history service")
    except Exception as e:
        logger.error(f"Error loading available verses: {e}")


def show_current_year_stats():
    """Show verse usage statistics for current year."""
    # Ensure available verses are loaded
    load_available_verses()
    
    stats = verse_history.get_stats()
    
    print("📊 Current Year Verse Usage Statistics")
    print("=" * 50)
    print(f"Year: {stats['year']}")
    print(f"Total verses available: {stats['total_verses']}")
    print(f"Verses already sent: {stats['used_verses']}")
    print(f"Verses remaining: {stats['unused_verses']}")
    print(f"Completion: {stats['completion_percentage']:.1f}%")
    print()
    
    if stats['used_verses'] > 0:
        print("📋 Recently sent verses this year:")
        print("-" * 40)
        # Show last 5 sent verses for current year
        current_year = verse_history.get_current_year()
        sent_verses = list(verse_history.get_sent_verses_for_year(current_year))
        for i, reference in enumerate(sent_verses[-5:], 1):
            print(f"{i}. {reference}")
        print()
    
    if stats['unused_verses'] > 0:
        print("📖 Available verses for this year:")
        print("-" * 40)
        unused_verses = verse_history.get_unused_verses_for_year(current_year)
        for i, verse in enumerate(unused_verses[:5], 1):  # Show first 5
            print(f"{i}. {verse.reference}")
        if len(unused_verses) > 5:
            print(f"... and {len(unused_verses) - 5} more")
        print()


def show_all_years_stats():
    """Show verse usage statistics for all years."""
    # Ensure available verses are loaded
    load_available_verses()
    
    all_stats = verse_history.get_all_years_stats()
    
    if not all_stats:
        print("📊 No verse history found for any year.")
        return
    
    print("📊 All Years Verse Usage Statistics")
    print("=" * 50)
    
    for year in sorted(all_stats.keys(), reverse=True):
        stats = all_stats[year]
        print(f"\nYear {year}:")
        print(f"  Verses sent: {stats['used_verses']}/{stats['total_verses']}")
        print(f"  Completion: {stats['completion_percentage']:.1f}%")
    
    print()


def show_detailed_year_stats(year: int):
    """Show detailed statistics for a specific year."""
    # Ensure available verses are loaded
    load_available_verses()
    
    stats = verse_history.get_stats(year)
    
    print(f"📊 Detailed Statistics for Year {year}")
    print("=" * 50)
    print(f"Total verses available: {stats['total_verses']}")
    print(f"Verses already sent: {stats['used_verses']}")
    print(f"Verses remaining: {stats['unused_verses']}")
    print(f"Completion: {stats['completion_percentage']:.1f}%")
    print()
    
    if stats['used_verses'] > 0:
        print(f"📋 All verses sent in {year}:")
        print("-" * 40)
        sent_verses = list(verse_history.get_sent_verses_for_year(year))
        for i, reference in enumerate(sent_verses, 1):
            print(f"{i}. {reference}")
        print()
    
    if stats['unused_verses'] > 0:
        print(f"📖 Available verses for {year}:")
        print("-" * 40)
        unused_verses = verse_history.get_unused_verses_for_year(year)
        for i, verse in enumerate(unused_verses[:10], 1):  # Show first 10
            print(f"{i}. {verse.reference}")
        if len(unused_verses) > 10:
            print(f"... and {len(unused_verses) - 10} more")
        print()


def reset_current_year_history():
    """Reset verse history for current year."""
    current_year = verse_history.get_current_year()
    print(f"🔄 Resetting verse history for year {current_year}...")
    verse_history.reset_history_for_year(current_year)
    print(f"✅ Verse history for year {current_year} has been reset!")
    print("All verses are now available again for this year.")
    print()


def reset_all_history():
    """Reset all verse history."""
    print("🔄 Resetting all verse history...")
    verse_history.reset_all_history()
    print("✅ All verse history has been reset!")
    print("All verses are now available again for all years.")
    print()


def cleanup_old_years():
    """Clean up history for old years."""
    print("🧹 Cleaning up old years history...")
    verse_history.cleanup_old_years()
    print("✅ Old years history cleaned up!")
    print()


def main():
    """Main function."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "reset":
            reset_current_year_history()
        elif command == "reset-all":
            reset_all_history()
        elif command == "stats":
            show_current_year_stats()
        elif command == "all-years":
            show_all_years_stats()
        elif command == "year" and len(sys.argv) > 2:
            try:
                year = int(sys.argv[2])
                show_detailed_year_stats(year)
            except ValueError:
                print("❌ Invalid year. Please provide a valid year number.")
                return 1
        elif command == "cleanup":
            cleanup_old_years()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands:")
            print("  stats          - Show current year statistics")
            print("  all-years      - Show statistics for all years")
            print("  year <year>    - Show detailed statistics for specific year")
            print("  reset          - Reset current year history")
            print("  reset-all      - Reset all history")
            print("  cleanup        - Clean up old years history")
            return 1
    else:
        show_current_year_stats()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1) 