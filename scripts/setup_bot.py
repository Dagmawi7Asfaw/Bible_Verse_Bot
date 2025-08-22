#!/usr/bin/env python3
"""
Setup script for the Bible Verse Telegram Bot.
Helps users configure the bot with their Telegram credentials.
"""

import os
import sys
from pathlib import Path

def get_bot_token():
    """Get bot token from user input."""
    print("\n=== Telegram Bot Token Setup ===")
    print("1. Go to @BotFather on Telegram")
    print("2. Send /newbot command")
    print("3. Follow the instructions to create your bot")
    print("4. Copy the token provided by BotFather")
    print()
    
    token = input("Enter your bot token: ").strip()
    
    if not token:
        print("❌ Bot token is required!")
        return None
    
    return token

def get_chat_id():
    """Get chat ID from user input."""
    print("\n=== Chat ID Setup ===")
    print("1. Add your bot to the group/channel where you want verses sent")
    print("2. Make sure the bot has permission to send messages")
    print("3. Send a message in the group/channel")
    print("4. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
    print("5. Look for 'chat' -> 'id' in the response")
    print()
    
    chat_id = input("Enter the chat ID: ").strip()
    
    if not chat_id:
        print("❌ Chat ID is required!")
        return None
    
    return chat_id

def get_schedule_time():
    """Get schedule time from user input."""
    print("\n=== Schedule Setup ===")
    print("Enter the time when you want daily verses to be sent (24-hour format)")
    print("Example: 09:00 for 9:00 AM")
    print()
    
    time_input = input("Enter schedule time (HH:MM): ").strip()
    
    if not time_input:
        print("Using default time: 09:00")
        return "09:00"
    
    # Validate time format
    try:
        hour, minute = map(int, time_input.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
    except (ValueError, AttributeError):
        print("❌ Invalid time format! Using default: 09:00")
        return "09:00"
    
    return time_input

def create_env_file():
    """Create .env file with user configuration."""
    print("\n=== Bible Verse Bot Setup ===")
    print("This script will help you configure your bot.")
    print()
    
    # Get configuration from user
    bot_token = get_bot_token()
    if not bot_token:
        return False
    
    chat_id = get_chat_id()
    if not chat_id:
        return False
    
    schedule_time = get_schedule_time()
    
    # Create .env file
    env_content = f"""# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={bot_token}
TELEGRAM_CHAT_ID={chat_id}

# Bible API Configuration
# Using free wldeh/bible-api CDN - no API key required!

# Bot Settings
VERSE_SCHEDULE_TIME={schedule_time}
VERSE_SCHEDULE_TIMEZONE=UTC
LOG_LEVEL=INFO

# Database/Storage (optional for future use)
DATABASE_URL=sqlite:///data/bible_bot.db
"""
    
    # Write to .env file
    env_file = Path(".env")
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Configuration saved to {env_file}")
    print("\n=== Next Steps ===")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Test the bot: python src/main.py --test")
    print("3. Run the bot: python src/main.py")
    print("\nHappy verse sharing! 🙏")
    
    return True

def main():
    """Main setup function."""
    try:
        success = create_env_file()
        if not success:
            print("\n❌ Setup failed. Please try again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 