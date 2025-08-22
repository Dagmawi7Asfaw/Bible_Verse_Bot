#!/usr/bin/env python3
"""
Script to check which groups the bot is currently in and get information about them.
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_bot_groups():
    """Check which groups the bot is in and get their information."""
    
    # Get bot token from environment
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ No bot token found in .env file")
        return
    
    # Get chat IDs from environment
    chat_ids_str = os.getenv('TELEGRAM_CHAT_IDS', '')
    if not chat_ids_str:
        print("❌ No chat IDs found in .env file")
        return
    
    chat_ids = [cid.strip() for cid in chat_ids_str.split(',') if cid.strip()]
    
    print(f"🤖 Bot Token: {bot_token[:10]}...")
    print(f"📱 Configured Chat IDs: {len(chat_ids)}")
    print()
    
    async with aiohttp.ClientSession() as session:
        for chat_id in chat_ids:
            await check_chat_info(session, bot_token, chat_id)
    
    print("\n" + "="*50)
    print("🔍 To see recent bot activity, send a message in any group")
    print("🔍 Then run: python scripts/check_groups.py --updates")

async def check_chat_info(session, bot_token, chat_id):
    """Get information about a specific chat."""
    
    try:
        # Get chat information
        url = f"https://api.telegram.org/bot{bot_token}/getChat"
        params = {"chat_id": chat_id}
        
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                if data["ok"]:
                    chat = data["result"]
                    chat_type = chat.get("type", "unknown")
                    title = chat.get("title", chat.get("first_name", "Unknown"))
                    username = chat.get("username", "No username")
                    
                    print(f"📋 Chat ID: {chat_id}")
                    print(f"   Type: {chat_type}")
                    print(f"   Name: {title}")
                    print(f"   Username: @{username}" if username != "No username" else "   Username: No username")
                    
                    # Check if bot is member
                    await check_bot_member(session, bot_token, chat_id)
                    print()
                else:
                    print(f"❌ Failed to get chat info for {chat_id}: {data.get('description', 'Unknown error')}")
            else:
                print(f"❌ HTTP error {response.status} for chat {chat_id}")
                
    except Exception as e:
        print(f"❌ Error checking chat {chat_id}: {e}")

async def check_bot_member(session, bot_token, chat_id):
    """Check if the bot is a member of the chat."""
    
    try:
        # Get chat member info
        url = f"https://api.telegram.org/bot{bot_token}/getChatMember"
        params = {"chat_id": chat_id, "user_id": bot_token.split(':')[0]}
        
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                if data["ok"]:
                    member = data["result"]
                    status = member.get("status", "unknown")
                    permissions = member.get("can_send_messages", False)
                    
                    print(f"   Bot Status: {status}")
                    print(f"   Can Send Messages: {'✅ Yes' if permissions else '❌ No'}")
                else:
                    print(f"   Bot Status: ❌ Not a member")
            else:
                print(f"   Bot Status: ❌ Error checking membership")
                
    except Exception as e:
        print(f"   Bot Status: ❌ Error: {e}")

async def check_recent_updates():
    """Check recent bot updates to see active groups."""
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ No bot token found in .env file")
        return
    
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        params = {"limit": 100}  # Get last 100 updates
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data["ok"]:
                        updates = data["result"]
                        
                        if not updates:
                            print("📭 No recent updates found")
                            print("💡 Send a message in any group where the bot is added to see activity")
                            return
                        
                        print(f"📱 Recent Updates: {len(updates)} found")
                        print()
                        
                        # Group updates by chat
                        chat_updates = {}
                        for update in updates:
                            if "message" in update:
                                chat = update["message"]["chat"]
                                chat_id = str(chat["id"])
                                if chat_id not in chat_updates:
                                    chat_updates[chat_id] = {
                                        "chat": chat,
                                        "updates": []
                                    }
                                chat_updates[chat_id]["updates"].append(update)
                        
                        for chat_id, info in chat_updates.items():
                            chat = info["chat"]
                            updates_count = len(info["updates"])
                            
                            print(f"💬 Chat ID: {chat_id}")
                            print(f"   Type: {chat.get('type', 'unknown')}")
                            print(f"   Name: {chat.get('title', chat.get('first_name', 'Unknown'))}")
                            print(f"   Recent Activity: {updates_count} updates")
                            print()
                    else:
                        print(f"❌ API Error: {data.get('description', 'Unknown error')}")
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error checking updates: {e}")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--updates":
        print("🔍 Checking recent bot updates...")
        asyncio.run(check_recent_updates())
    else:
        print("🔍 Checking bot group information...")
        asyncio.run(check_bot_groups())

if __name__ == "__main__":
    main() 