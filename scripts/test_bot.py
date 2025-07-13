#!/usr/bin/env python3
"""
Test script for the Bible Verse Telegram Bot.
Tests basic functionality without sending actual messages.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.bible_api import BibleAPIService
from src.models.verse import VerseRequest
from src.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger()
logger = get_logger(__name__)


async def test_bible_api():
    """Test the Bible API service."""
    print("🧪 Testing Bible API Service...")
    
    try:
        async with BibleAPIService() as service:
            # Test random verse
            print("  - Testing random verse...")
            request = VerseRequest(random=True, translation="NIV")
            response = await service.get_verse(request)
            
            if response.success and response.verse:
                print(f"    ✅ Random verse: {response.verse.reference}")
                print(f"       Text: {response.verse.text[:50]}...")
            else:
                print(f"    ❌ Failed to get random verse: {response.error}")
                return False
            
            # Test specific verse
            print("  - Testing specific verse...")
            request = VerseRequest(reference="John 3:16", translation="NIV")
            response = await service.get_verse(request)
            
            if response.success and response.verse:
                print(f"    ✅ Specific verse: {response.verse.reference}")
            else:
                print(f"    ❌ Failed to get specific verse: {response.error}")
                return False
            
            # Test daily verse
            print("  - Testing daily verse...")
            response = await service.get_daily_verse()
            
            if response.success and response.verse:
                print(f"    ✅ Daily verse: {response.verse.reference}")
            else:
                print(f"    ❌ Failed to get daily verse: {response.error}")
                return False
        
        print("✅ Bible API tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Bible API test failed: {e}")
        return False


async def test_configuration():
    """Test configuration loading."""
    print("🧪 Testing Configuration...")
    
    try:
        from src.config.settings import get_settings
        
        settings = get_settings()
        
        # Check required settings
        if not settings.telegram_bot_token:
            print("  ⚠️  No Telegram bot token configured")
        else:
            print("  ✅ Telegram bot token configured")
        
        if not settings.telegram_chat_id:
            print("  ⚠️  No Telegram chat ID configured")
        else:
            print("  ✅ Telegram chat ID configured")
        
        print(f"  ✅ Schedule time: {settings.verse_schedule_time}")
        print(f"  ✅ Log level: {settings.log_level}")
        
        print("✅ Configuration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Starting Bible Verse Bot Tests...\n")
    
    # Test configuration
    config_ok = await test_configuration()
    print()
    
    # Test Bible API
    api_ok = await test_bible_api()
    print()
    
    # Summary
    if config_ok and api_ok:
        print("🎉 All tests passed! Your bot is ready to run.")
        print("\nNext steps:")
        print("1. Configure your .env file with Telegram credentials")
        print("2. Run: python src/main.py --test")
        print("3. Run: python src/main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
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