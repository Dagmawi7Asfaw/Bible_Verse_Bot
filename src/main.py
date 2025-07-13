"""
Main entry point for the Bible Verse Telegram Bot.
Handles startup, configuration, and main application loop.
"""

import asyncio
import signal
import sys
from pathlib import Path

from src.bot.telegram_bot import BibleVerseBot
from src.config.settings import get_settings
from src.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger()
logger = get_logger(__name__)


class BibleVerseBotApp:
    """Main application class for the Bible Verse Bot."""
    
    def __init__(self):
        self.settings = get_settings()
        self.bot = BibleVerseBot()
        self.running = False
        
    async def start(self):
        """Start the bot application."""
        try:
            logger.info("Starting Bible Verse Bot...")
            
            # Test connection
            if not await self.bot.test_connection():
                logger.error("Failed to connect to Telegram. Please check your configuration.")
                return False
            
            # Schedule daily verse
            self.bot.schedule_daily_verse()
            
            # Set running flag
            self.running = True
            
            logger.info("Bot started successfully!")
            logger.info(f"Daily verses will be sent at {self.settings.verse_schedule_time}")
            
            # Run the scheduler
            await self.bot.run_scheduler()
            
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            return False
        
        return True
    
    async def stop(self):
        """Stop the bot application."""
        logger.info("Stopping Bible Verse Bot...")
        self.running = False
    
    async def send_test_verse(self):
        """Send a test verse immediately."""
        try:
            logger.info("Sending test verse...")
            success = await self.bot.send_daily_verse()
            
            if success:
                logger.info("Test verse sent successfully!")
            else:
                logger.error("Failed to send test verse")
                
        except Exception as e:
            logger.error(f"Error sending test verse: {e}")


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


async def main():
    """Main application entry point."""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start the application
    app = BibleVerseBotApp()
    
    # Check if we should send a test verse
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        await app.send_test_verse()
        return
    
    # Start the application
    await app.start()


if __name__ == "__main__":
    try:
        # Run the main application
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1) 