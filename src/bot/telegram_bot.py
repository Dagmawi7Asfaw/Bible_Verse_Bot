"""
Telegram bot for sending Bible verses.
Handles message sending, scheduling, and bot interactions.
"""

import asyncio
import schedule
import time
from datetime import datetime
from typing import Optional

from telegram import Bot
from telegram.error import TelegramError

from src.config.settings import get_settings
from src.models.verse import BibleVerse, VerseRequest
from src.services.bible_api import BibleAPIService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BibleVerseBot:
    """Telegram bot for sending Bible verses."""
    
    def __init__(self):
        self.settings = get_settings()
        self.bot = Bot(token=self.settings.telegram_bot_token)
        self.chat_id = self.settings.telegram_chat_id
        self.chat_ids = self.settings.telegram_chat_ids
        self.bible_service = BibleAPIService()
        
    async def send_verse(self, verse: BibleVerse, chat_id: str = None) -> bool:
        """
        Send a Bible verse to a specific chat or all configured chats.
        
        Args:
            verse: Bible verse to send
            chat_id: Specific chat ID to send to (if None, sends to all configured chats)
            
        Returns:
            True if sent successfully to at least one chat, False otherwise
        """
        try:
            # Format the message
            message = self._format_verse_message(verse)
            
            # Determine which chats to send to
            target_chats = [chat_id] if chat_id else self.chat_ids
            
            if not target_chats:
                logger.warning("No chat IDs configured")
                return False
            
            success_count = 0
            total_chats = len(target_chats)
            
            # Send to each chat
            for cid in target_chats:
                try:
                    await self.bot.send_message(
                        chat_id=cid,
                        text=message,
                        parse_mode='HTML'
                    )
                    logger.info(f"Successfully sent verse to chat {cid}: {verse.reference}")
                    success_count += 1
                    
                except TelegramError as e:
                    logger.error(f"Failed to send verse to chat {cid}: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error sending verse to chat {cid}: {e}")
            
            if success_count > 0:
                logger.info(f"Sent verse to {success_count}/{total_chats} chats")
                return True
            else:
                logger.error("Failed to send verse to any chat")
                return False
            
        except Exception as e:
            logger.error(f"Unexpected error in send_verse: {e}")
            return False
    
    def _format_verse_message(self, verse: BibleVerse) -> str:
        """
        Format a Bible verse for Telegram message.
        
        Args:
            verse: Bible verse to format
            
        Returns:
            Formatted message string
        """
        # Create a beautiful formatted message
        message = f"""
📖 <b>Daily Bible Verse</b>

<i>"{verse.text}"</i>

<b>— {verse.reference} ({verse.translation})</b>

Have a blessed day! 🙏
        """.strip()
        
        return message
    
    async def send_daily_verse(self) -> bool:
        """
        Send the daily verse.
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            logger.info("Fetching daily verse...")
            
            # Get a verse
            response = await self.bible_service.get_daily_verse()
            
            if not response.success or not response.verse:
                logger.error(f"Failed to get daily verse: {response.error}")
                return False
            
            # Send the verse
            return await self.send_verse(response.verse)
            
        except Exception as e:
            logger.error(f"Error in send_daily_verse: {e}")
            return False
    
    async def send_custom_verse(self, reference: str, translation: str = "NIV") -> bool:
        """
        Send a specific verse by reference.
        
        Args:
            reference: Verse reference (e.g., "John 3:16")
            translation: Bible translation
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            logger.info(f"Fetching verse: {reference}")
            
            # Create request
            request = VerseRequest(
                reference=reference,
                translation=translation
            )
            
            # Get verse
            response = await self.bible_service.get_verse(request)
            
            if not response.success or not response.verse:
                logger.error(f"Failed to get verse {reference}: {response.error}")
                return False
            
            # Send the verse
            return await self.send_verse(response.verse)
            
        except Exception as e:
            logger.error(f"Error in send_custom_verse: {e}")
            return False
    
    def schedule_daily_verse(self):
        """Schedule the daily verse sending for all configured times."""
        schedule_times = self.settings.verse_schedule_times
        if not schedule_times:
            schedule_times = [self.settings.verse_schedule_time]

        logger.info(f"Scheduling daily verse for times: {schedule_times}")

        for t in schedule_times:
            schedule.every().day.at(t).do(
                lambda: asyncio.run(self.send_daily_verse())
            )
    
    async def run_scheduler(self):
        """Run the scheduler loop."""
        logger.info("Starting scheduler...")
        
        while True:
            try:
                schedule.run_pending()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in scheduler: {e}")
                await asyncio.sleep(60)
    
    async def test_connection(self) -> bool:
        """
        Test the bot connection and permissions.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Get bot info
            bot_info = await self.bot.get_me()
            logger.info(f"Bot connected: @{bot_info.username}")
            
            # Test sending a message to all configured chats
            test_message = "🤖 Bible Verse Bot is online and ready!"
            success_count = 0
            total_chats = len(self.chat_ids)
            
            for chat_id in self.chat_ids:
                try:
                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=test_message
                    )
                    logger.info(f"Connection test successful for chat {chat_id}")
                    success_count += 1
                except TelegramError as e:
                    logger.error(f"Connection test failed for chat {chat_id}: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error in connection test for chat {chat_id}: {e}")
            
            if success_count > 0:
                logger.info(f"Connection test successful for {success_count}/{total_chats} chats")
                return True
            else:
                logger.error("Connection test failed for all chats")
                return False
            
        except Exception as e:
            logger.error(f"Unexpected error in connection test: {e}")
            return False


# Convenience functions
async def send_verse_to_telegram(verse: BibleVerse, chat_id: str = None) -> bool:
    """Convenience function to send a verse to Telegram."""
    bot = BibleVerseBot()
    return await bot.send_verse(verse, chat_id)


async def send_daily_verse_to_telegram() -> bool:
    """Convenience function to send daily verse to Telegram."""
    bot = BibleVerseBot()
    return await bot.send_daily_verse() 