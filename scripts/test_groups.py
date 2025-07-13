#!/usr/bin/env python3
"""
Test script to send messages to each configured group individually.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.bot.telegram_bot import BibleVerseBot
from src.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger()
logger = get_logger(__name__)


async def test_individual_groups():
    """Test sending messages to each group individually."""
    print("🧪 Testing Individual Groups...")
    print("=" * 40)
    
    bot = BibleVerseBot()
    
    # Test each chat ID individually
    for i, chat_id in enumerate(bot.chat_ids, 1):
        print(f"\n📱 Testing Group {i}: {chat_id}")
        
        try:
            # Test connection
            test_message = f"🤖 Test message to group {i}"
            await bot.bot.send_message(
                chat_id=chat_id,
                text=test_message
            )
            print(f"  ✅ Success! Message sent to group {i}")
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Group testing completed!")


async def main():
    """Main function."""
    try:
        await test_individual_groups()
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1) 