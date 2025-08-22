#!/usr/bin/env python3
"""
Script to test if the bot can send messages to configured groups.
"""

import os
import asyncio
from dotenv import load_dotenv
from src.bot.telegram_bot import BibleVerseBot
from src.models.verse import BibleVerse

# Load environment variables
load_dotenv()

async def test_bot_permissions():
    """Test if the bot can send messages to all configured groups."""
    
    print("🔍 Testing bot permissions and message sending...")
    print()
    
    try:
        # Create bot instance
        bot = BibleVerseBot()
        
        # Test connection first
        print("📡 Testing bot connection...")
        if not await bot.test_connection():
            print("❌ Bot connection failed!")
            return
        
        print("✅ Bot connection successful!")
        print()
        
        # Test sending a test verse to each group
        print("📤 Testing verse sending to each group...")
        print()
        
        # Create a test verse
        test_verse = BibleVerse(
            reference="Test Message",
            text="🔍 **Permission Test**\n\nThis is a test message to verify the bot can send messages to this group.\n\nIf you see this, the bot has proper permissions! ✅",
            translation="TEST",
            book="Test",
            chapter=1,
            verse=1
        )
        
        for chat_id in bot.chat_ids:
            try:
                print(f"📱 Testing chat ID: {chat_id}")
                
                # Try to send the test verse
                success = await bot.send_verse(test_verse, chat_id)
                
                if success:
                    print(f"   ✅ Verse sent successfully!")
                else:
                    print(f"   ❌ Failed to send verse")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print()
        
        print("🎯 Permission test completed!")
        print()
        print("💡 If verses failed to send, you need to:")
        print("   1. Go to each group")
        print("   2. Edit group settings")
        print("   3. Find your bot in admin list")
        print("   4. Enable 'Send Messages' permission")
        
    except Exception as e:
        print(f"❌ Error during permission test: {e}")

def main():
    """Main function."""
    asyncio.run(test_bot_permissions())

if __name__ == "__main__":
    main() 