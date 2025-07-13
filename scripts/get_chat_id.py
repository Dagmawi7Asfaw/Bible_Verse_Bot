#!/usr/bin/env python3
"""
Simple script to get chat ID using your bot token.
"""

import requests
import json

def get_chat_id(bot_token):
    """Get chat ID from bot updates."""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if not data.get('ok'):
            print(f"❌ Error: {data.get('description', 'Unknown error')}")
            return None
        
        updates = data.get('result', [])
        
        if not updates:
            print("❌ No updates found!")
            print("\nTo get updates:")
            print("1. Add your bot to a group")
            print("2. Send a message in the group")
            print("3. Run this script again")
            return None
        
        print("📋 Found updates:")
        print("=" * 50)
        
        for i, update in enumerate(updates):
            if 'message' in update:
                chat = update['message']['chat']
                chat_id = chat['id']
                chat_type = chat.get('type', 'unknown')
                chat_title = chat.get('title', chat.get('first_name', 'Unknown'))
                
                print(f"Update {i+1}:")
                print(f"  Chat ID: {chat_id}")
                print(f"  Type: {chat_type}")
                print(f"  Name: {chat_title}")
                print()
        
        return updates
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main function."""
    print("🔍 Telegram Chat ID Finder")
    print("=" * 30)
    
    # Your bot token
    bot_token = "7595841385:AAEFQXMpW2eIAnkUbRTyN8F0jTudwZqXRXo"
    
    print(f"Using bot token: {bot_token[:20]}...")
    print()
    
    updates = get_chat_id(bot_token)
    
    if updates:
        print("✅ Copy the Chat ID you want to use!")
        print("\nNext steps:")
        print("1. Copy the Chat ID from above")
        print("2. Run: python scripts/setup_bot.py")
        print("3. Enter your bot token and the Chat ID")

if __name__ == "__main__":
    main() 