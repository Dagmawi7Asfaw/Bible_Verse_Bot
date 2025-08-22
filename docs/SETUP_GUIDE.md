# Bible Verse Bot Setup Guide

This guide will walk you through setting up and running your Bible Verse Telegram Bot.

## Prerequisites

- Python 3.8 or higher
- A Telegram account
- Basic knowledge of command line operations

## Step 1: Clone and Setup

1. **Clone the repository** (if you haven't already):

   ```bash
   git clone <repository-url>
   cd Bible_verse_bot
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Step 2: Create Your Telegram Bot

1. **Open Telegram** and search for `@BotFather`

2. **Start a chat** with BotFather and send `/newbot`

3. **Follow the instructions**:
   - Choose a name for your bot (e.g., "Daily Bible Verses")
   - Choose a username (must end with 'bot', e.g., "daily_bible_verses_bot")

4. **Save the bot token** that BotFather provides (you'll need this later)

## Step 3: Get Your Chat ID

### Method 1: Using the Bot API (Recommended)

1. **Add your bot to the group/channel** where you want verses sent
2. **Make sure the bot has permission** to send messages
3. **Send a message** in the group/channel
4. **Visit this URL** (replace `YOUR_BOT_TOKEN` with your actual token):

   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```

5. **Look for the chat ID** in the response:

   ```json
   {
     "message": {
       "chat": {
         "id": -1001234567890,  // This is your chat ID
         "title": "Your Group Name"
       }
     }
   }
   ```

### Method 2: Using a Helper Bot

1. **Search for `@userinfobot`** on Telegram
2. **Add it to your group/channel**
3. **It will show you the chat ID**

## Step 4: Configure the Bot

### Option A: Use the Setup Script (Recommended)

Run the interactive setup script:

```bash
python scripts/setup_bot.py
```

This will guide you through entering:

- Your bot token
- Your chat ID
- Your preferred schedule time

### Option B: Manual Configuration

1. **Copy the environment template**:

   ```bash
   cp env.example .env
   ```

2. **Edit the `.env` file** with your settings:

   ```bash
   nano .env
   ```

3. **Fill in your configuration**:

   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   VERSE_SCHEDULE_TIME=09:00
   ```

## Step 5: Test Your Bot

1. **Run the test script** to verify everything works:

   ```bash
   python scripts/test_bot.py
   ```

2. **Test sending a verse** (this will actually send a message):

   ```bash
   python src/main.py --test
   ```

## Step 6: Run the Bot

1. **Start the bot**:

   ```bash
   python src/main.py
   ```

2. **The bot will**:
   - Connect to Telegram
   - Send a startup message
   - Begin scheduling daily verses
   - Run continuously until stopped

3. **To stop the bot**, press `Ctrl+C`

## Step 7: Production Deployment

### Option A: Using systemd (Linux)

1. **Create a service file**:

   ```bash
   sudo nano /etc/systemd/system/bible-verse-bot.service
   ```

2. **Add the service configuration**:

   ```ini
   [Unit]
   Description=Bible Verse Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=your_username
   WorkingDirectory=/path/to/Bible_verse_bot
   Environment=PATH=/path/to/Bible_verse_bot/venv/bin
   ExecStart=/path/to/Bible_verse_bot/venv/bin/python src/main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service**:

   ```bash
   sudo systemctl enable bible-verse-bot
   sudo systemctl start bible-verse-bot
   ```

### Option B: Using Docker

1. **Create a Dockerfile**:

   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   CMD ["python", "src/main.py"]
   ```

2. **Build and run**:

   ```bash
   docker build -t bible-verse-bot .
   docker run -d --env-file .env bible-verse-bot
   ```

## Troubleshooting

### Common Issues

1. **"Bot token invalid"**
   - Double-check your bot token
   - Make sure there are no extra spaces

2. **"Chat not found"**
   - Verify your chat ID is correct
   - Make sure the bot is added to the group/channel
   - Check that the bot has permission to send messages

3. **"Permission denied"**
   - Make sure the bot is an admin in the group/channel
   - Check that the bot has "Send Messages" permission

4. **"Module not found"**
   - Make sure you're in the virtual environment
   - Run `pip install -r requirements.txt` again

### Logs

Check the logs for detailed error information:

```bash
tail -f data/logs/$(date +%Y-%m-%d).log
```

### Getting Help

If you're still having issues:

1. Check the logs in `data/logs/`
2. Run the test script: `python scripts/test_bot.py`
3. Open an issue on GitHub with your error details

## Customization

### Changing the Schedule

Edit your `.env` file:

```env
VERSE_SCHEDULE_TIME=18:00  # 6:00 PM
```

### Adding More Verses

Edit `src/services/bible_api.py` and add more verses to the `fallback_verses` list.

### Using the Bible API

The bot now uses the free [wldeh/bible-api](https://github.com/wldeh/bible-api) CDN service, which provides multiple Bible translations without requiring any API keys or authentication.

## Security Notes

- **Never share your bot token** publicly
- **Keep your `.env` file secure** and never commit it to version control
- **Use a dedicated bot** for this purpose, not your main bot

## Support

For additional help:

- Check the main README.md file
- Review the code comments
- Open an issue on GitHub

Happy verse sharing! 🙏
