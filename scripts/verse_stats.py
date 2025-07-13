#!/usr/bin/env python3
"""
Script to view and manage verse history statistics.
Shows which verses have been sent and which are still available.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.verse_history import verse_history
from src.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger()
logger = get_logger(__name__)


def show_stats():
    """Show verse usage statistics."""
    stats = verse_history.get_stats()
    
    print("📊 Verse Usage Statistics")
    print("=" * 40)
    print(f"Total verses available: {stats['total_verses']}")
    print(f"Verses already sent: {stats['used_verses']}")
    print(f"Verses remaining: {stats['unused_verses']}")
    print(f"Completion: {stats['completion_percentage']:.1f}%")
    print()
    
    if stats['used_verses'] > 0:
        print("📋 Recently sent verses:")
        print("-" * 30)
        # Show last 5 sent verses
        sent_list = list(verse_history.sent_verses)[-5:]
        for i, reference in enumerate(sent_list, 1):
            print(f"{i}. {reference}")
        print()
    
    if stats['unused_verses'] > 0:
        print("📖 Available verses:")
        print("-" * 30)
        unused_verses = verse_history.get_unused_verses()
        for i, verse in enumerate(unused_verses[:5], 1):  # Show first 5
            print(f"{i}. {verse.reference}")
        if len(unused_verses) > 5:
            print(f"... and {len(unused_verses) - 5} more")
        print()


def reset_history():
    """Reset verse history."""
    print("🔄 Resetting verse history...")
    verse_history.reset_history()
    print("✅ Verse history has been reset!")
    print("All verses are now available again.")
    print()


def main():
    """Main function."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "reset":
            reset_history()
        elif command == "stats":
            show_stats()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: stats, reset")
            return 1
    else:
        show_stats()
    
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