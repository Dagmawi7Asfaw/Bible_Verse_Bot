# 📖 Bible Verse Telegram Bot

A professional, feature-rich Telegram bot that automatically sends daily Bible verses to multiple groups and channels. Built with Python and the `python-telegram-bot` library, featuring multi-group support, comprehensive logging, and a modular architecture.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-blue.svg)](https://core.telegram.org/bots/api)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

- 🕐 **Scheduled Daily Verses**: Automatically sends Bible verses at configurable times
- 📱 **Multi-Group Support**: Send verses to multiple Telegram groups simultaneously
- 📖 **Multiple Bible APIs**: Support for various Bible translation APIs with fallback
- 🎯 **Highly Customizable**: Easy configuration for different groups, schedules, and preferences
- 📝 **Comprehensive Logging**: Detailed logging for monitoring and debugging
- 🔧 **Modular Design**: Clean, maintainable code structure with separation of concerns
- 🧪 **Built-in Testing**: Comprehensive test suite and validation scripts
- 🚀 **Production Ready**: Includes deployment guides and systemd service files

## 🏗️ Project Structure

```
Bible_verse_bot/
├── src/                    # Main source code
│   ├── bot/               # Telegram bot handlers and logic
│   ├── services/          # External API services (Bible APIs)
│   ├── utils/             # Utility functions and helpers
│   ├── config/            # Configuration management
│   ├── models/            # Data models and schemas
│   └── main.py            # Application entry point
├── scripts/               # Helper scripts and utilities
├── tests/                 # Unit and integration tests
├── docs/                  # Documentation and guides
├── data/                  # Data storage and logs
├── requirements.txt       # Python dependencies
├── env.example            # Environment variables template
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8** or higher
- **Git** for cloning the repository
- **A Telegram account** and bot token
- **Basic command line knowledge**

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Dagmawi7Asfaw/Bible_Verse_Bot.git
   cd Bible_Verse_Bot
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot**

   ```bash
   python scripts/setup_bot.py
   ```

5. **Test the bot**

   ```bash
   python scripts/test_bot.py
   ```

6. **Send a test verse**

   ```bash
   PYTHONPATH=. python src/main.py --test
   ```

7. **Run the bot**

   ```bash
   PYTHONPATH=. python src/main.py
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_IDS=chat_id_1,chat_id_2,chat_id_3

# Bible API Configuration
# Using free wldeh/bible-api CDN - no API key required!

# Bot Settings
VERSE_SCHEDULE_TIME=09:00
VERSE_SCHEDULE_TIMEZONE=UTC
LOG_LEVEL=INFO

# Database/Storage (Optional)
DATABASE_URL=sqlite:///data/bible_bot.db
```

### Getting Your Bot Token

1. **Open Telegram** and search for `@BotFather`
2. **Send `/newbot`** command
3. **Follow the instructions** to create your bot
4. **Save the token** provided by BotFather

### Getting Chat IDs

#### Method 1: Using the Bot API

1. Add your bot to the group/channel
2. Send a message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for the `chat.id` in the response

#### Method 2: Using Helper Bots

- Add `@userinfobot` to your group
- It will automatically show you the chat ID

#### Method 3: Using Our Script

```bash
python scripts/get_chat_id.py
```

## 📖 Usage

### Basic Commands

```bash
# Test the bot configuration
python scripts/test_bot.py

# Send a test verse to all groups
PYTHONPATH=. python src/main.py --test

# Run the bot for daily verses
PYTHONPATH=. python src/main.py

# Test individual groups
python scripts/test_groups.py
```

### Multi-Group Support

The bot supports sending verses to multiple groups simultaneously:

```env
TELEGRAM_CHAT_IDS=-1001234567890,-1009876543210,-1005556667777
```

Each group will receive the same verse at the scheduled time.

## 🔧 Customization

### Changing the Schedule

Edit your `.env` file:

```env
VERSE_SCHEDULE_TIME=18:00  # 6:00 PM
VERSE_SCHEDULE_TIMEZONE=America/New_York
```

### Adding More Verses

The bot now uses **true randomization** from the entire Bible! It automatically:

- **Picks random books** from all 66 books of the Bible
- **Selects random chapters** (avoiding chapter 1 for variety)
- **Chooses random verses** from each chapter
- **Rotates through 7 translations** weekly (KJV, ASV, BBE, DBY, WBT, WEB, YLT)
- **Tries up to 5 attempts** to find working verses

No more hardcoded verse lists - every day brings a fresh, truly random Bible verse!

```python
self.fallback_verses = [
    {
        "reference": "John 3:16",
        "text": "For God so loved the world...",
        "translation": "NIV",
        "book": "John",
        "chapter": 3,
        "verse": 16
    },
    # Add more verses here
]
```

### Using the Bible API

The bot now uses the free [wldeh/bible-api](https://github.com/wldeh/bible-api) CDN service, which provides multiple Bible translations without requiring any API keys or authentication.

## 🚀 Deployment

### Option 1: Using systemd (Linux)

1. **Create a service file**

   ```bash
   sudo nano /etc/systemd/system/bible-verse-bot.service
   ```

2. **Add the service configuration**

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

3. **Enable and start the service**

   ```bash
   sudo systemctl enable bible-verse-bot
   sudo systemctl start bible-verse-bot
   ```

### Option 2: Using Docker

1. **Create a Dockerfile**

   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   CMD ["python", "src/main.py"]
   ```

2. **Build and run**

   ```bash
   docker build -t bible-verse-bot .
   docker run -d --env-file .env bible-verse-bot
   ```

### Option 3: Using PM2 (Node.js)

1. **Install PM2**

   ```bash
   npm install -g pm2
   ```

2. **Create ecosystem file**

   ```javascript
   // ecosystem.config.js
   module.exports = {
     apps: [{
       name: 'bible-verse-bot',
       script: 'src/main.py',
       interpreter: './venv/bin/python',
       env: {
         PYTHONPATH: '.'
       }
     }]
   }
   ```

3. **Start with PM2**

   ```bash
   pm2 start ecosystem.config.js
   ```

## 🧪 Testing

### Run All Tests

```bash
python scripts/test_bot.py
```

### Test Individual Components

```bash
# Test Bible API service
pytest tests/test_bible_api.py

# Test group connectivity
python scripts/test_groups.py
```

### Manual Testing

```bash
# Test verse sending
PYTHONPATH=. python src/main.py --test

# Check logs
tail -f data/logs/$(date +%Y-%m-%d).log
```

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"Bot token invalid"** | Double-check your bot token from @BotFather |
| **"Chat not found"** | Verify chat ID and ensure bot is added to group |
| **"Permission denied"** | Make bot admin or give "Send Messages" permission |
| **"Module not found"** | Activate virtual environment and install requirements |
| **"Timed out"** | Check internet connection and Telegram API status |

### Logs

Check detailed logs for debugging:

```bash
tail -f data/logs/$(date +%Y-%m-%d).log
```

### Getting Help

1. **Check the logs** in `data/logs/`
2. **Run the test script**: `python scripts/test_bot.py`
3. **Review the setup guide**: `docs/SETUP_GUIDE.md`
4. **Open an issue** on GitHub with error details

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**

   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
4. **Add tests** for new functionality
5. **Commit your changes**

   ```bash
   git commit -m 'Add amazing feature'
   ```

6. **Push to the branch**

   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/Bible_Verse_Bot.git
cd Bible_Verse_Bot

# Add upstream remote
git remote add upstream https://github.com/Dagmawi7Asfaw/Bible_Verse_Bot.git

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python scripts/test_bot.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Telegram Bot API** for the messaging platform
- **Bible API** for verse data
- **Python Telegram Bot** library contributors
- **Open source community** for inspiration and tools

## 📞 Support

- **Documentation**: [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/Dagmawi7Asfaw/Bible_Verse_Bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Dagmawi7Asfaw/Bible_Verse_Bot/discussions)

---

**Made with ❤️ for spreading God's Word through technology**

⭐ **Star this repository if it helped you!**
