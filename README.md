# Bible Verse Telegram Bot

A professional Telegram bot that automatically sends daily Bible verses to a specified group or channel. Built with Python and the python-telegram-bot library.

## Features

- 🕐 **Scheduled Daily Verses**: Automatically sends Bible verses at a specified time
- 📖 **Multiple Bible APIs**: Support for various Bible translation APIs
- 🎯 **Customizable**: Easy configuration for different groups, schedules, and preferences
- 📝 **Logging**: Comprehensive logging for monitoring and debugging
- 🔧 **Modular Design**: Clean, maintainable code structure

## Project Structure

```
Bible_verse_bot/
├── src/
│   ├── bot/           # Telegram bot handlers and logic
│   ├── services/      # External API services (Bible APIs)
│   ├── utils/         # Utility functions and helpers
│   ├── config/        # Configuration management
│   └── models/        # Data models and schemas
├── tests/             # Unit and integration tests
├── docs/              # Documentation
├── scripts/           # Utility scripts
├── data/              # Data storage and logs
│   ├── bible_verses/  # Cached Bible verses
│   └── logs/          # Application logs
├── requirements.txt   # Python dependencies
├── env.example        # Environment variables template
└── README.md         # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- A Telegram bot token (get from [@BotFather](https://t.me/botfather))
- A Bible API key (optional, for enhanced functionality)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd Bible_verse_bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
nano .env
```

Required environment variables:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: The chat ID where verses will be sent
- `VERSE_SCHEDULE_TIME`: Time to send verses (format: HH:MM)

### 4. Running the Bot

```bash
# Run the bot
python src/main.py
```

## Usage

1. **Add the bot to your group/channel**: Make sure the bot has permission to send messages
2. **Configure the schedule**: Set the desired time in the `.env` file
3. **Start the bot**: The bot will automatically send verses at the scheduled time

## API Integration

The bot supports multiple Bible APIs:

- Bible API (scripture.api.bible)
- Bible Gateway API
- Local verse database

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub or contact the maintainers.
