#!/usr/bin/env python3
"""
Migration script to convert old verse history format to new year-based format.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.verse_history import verse_history
from src.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger()
logger = get_logger(__name__)


def migrate_old_history():
    """Migrate old verse history format to new year-based format."""
    history_file = Path("data/verse_history.json")
    
    if not history_file.exists():
        print("✅ No old history file found. Migration not needed.")
        return
    
    try:
        # Read old format
        with open(history_file, 'r') as f:
            old_data = json.load(f)
        
        if 'sent_verses_by_year' in old_data:
            print("✅ History file is already in new format. Migration not needed.")
            return
        
        # Get old sent verses
        old_sent_verses = old_data.get('sent_verses', [])
        last_updated = old_data.get('last_updated', datetime.now().isoformat())
        
        if not old_sent_verses:
            print("✅ No verses to migrate. Migration not needed.")
            return
        
        # Determine the year from last_updated or use current year
        try:
            update_date = datetime.fromisoformat(last_updated)
            year = update_date.year
        except:
            year = datetime.now().year
        
        print(f"🔄 Migrating {len(old_sent_verses)} verses from old format to year {year}...")
        
        # Create new format
        new_data = {
            'sent_verses_by_year': {
                str(year): old_sent_verses
            },
            'last_updated': datetime.now().isoformat()
        }
        
        # Backup old file
        backup_file = history_file.with_suffix('.json.backup')
        with open(backup_file, 'w') as f:
            json.dump(old_data, f, indent=2)
        print(f"📁 Old history backed up to {backup_file}")
        
        # Write new format
        with open(history_file, 'w') as f:
            json.dump(new_data, f, indent=2)
        
        print(f"✅ Successfully migrated {len(old_sent_verses)} verses to year {year}")
        print("🔄 Reloading verse history service...")
        
        # Reload the verse history service
        verse_history.load_history()
        
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False
    
    return True


def main():
    """Main function."""
    print("🔄 Verse History Migration Tool")
    print("=" * 40)
    
    success = migrate_old_history()
    
    if success:
        print("\n📊 Migration Summary:")
        print("- Old format: single list of sent verses")
        print("- New format: verses organized by year")
        print("- Benefits: No repetition within a year, fresh start each year")
        print("\nYou can now use the new commands:")
        print("  python scripts/verse_stats.py stats          - Show current year")
        print("  python scripts/verse_stats.py all-years      - Show all years")
        print("  python scripts/verse_stats.py year 2024      - Show specific year")
        print("  python scripts/verse_stats.py reset          - Reset current year")
        print("  python scripts/verse_stats.py reset-all      - Reset all years")
    
    return 0 if success else 1


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