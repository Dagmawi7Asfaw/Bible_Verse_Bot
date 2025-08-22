import asyncio
import os
from dotenv import load_dotenv

# Ensure project modules can be imported when running on Vercel
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables (Vercel env vars take precedence; dotenv is a noop locally if not present)
load_dotenv()

from src.bot.telegram_bot import BibleVerseBot  # noqa: E402


async def _send_daily():
	bot = BibleVerseBot()
	# Optional: ensure bot connectivity before sending
	await bot.test_connection()
	await bot.send_daily_verse()


def handler(request):
	"""Vercel serverless function entrypoint.
	- GET/POST /api/send_daily_verse triggers sending a daily verse to all configured chats.
	Returns a simple JSON response.
	"""
	try:
		asyncio.run(_send_daily())
		return {
			"status": 200,
			"headers": {"content-type": "application/json"},
			"body": "{\"ok\":true,\"message\":\"Daily verse sent\"}"
		}
	except Exception as e:
		return {
			"status": 500,
			"headers": {"content-type": "application/json"},
			"body": f"{{\"ok\":false,\"error\":\"{str(e)}\"}}"
		} 