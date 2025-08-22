#!/bin/bash

# Bible Verse Bot - Bash Script Version
# This script sends Bible verses to configured Telegram groups at scheduled times

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Load environment variables
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(cat "$PROJECT_DIR/.env" | grep -v '^#' | xargs)
else
    echo "❌ .env file not found in $PROJECT_DIR"
    exit 1
fi

# Check required environment variables
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN not set"
    exit 1
fi

if [ -z "$TELEGRAM_CHAT_IDS" ]; then
    echo "❌ TELEGRAM_CHAT_IDS not set"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Function to send a verse to a chat
send_verse_to_chat() {
    local chat_id="$1"
    local verse_text="$2"
    
    # Send message using Telegram Bot API
    local response=$(curl -s -X POST \
        "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d "chat_id=$chat_id" \
        -d "text=$verse_text" \
        -d "parse_mode=HTML" \
        -d "disable_web_page_preview=true")
    
    # Check if message was sent successfully
    if echo "$response" | grep -q '"ok":true'; then
        log "✅ Verse sent to chat $chat_id"
        return 0
    else
        error "Failed to send verse to chat $chat_id: $response"
        return 1
    fi
}

# Function to get a random Bible verse
get_random_verse() {
    # Array of popular Bible verses with translations
    local verses=(
        "📖 <b>John 3:16 (KJV)</b>\n\nFor God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."
        "📖 <b>Psalm 23:1 (KJV)</b>\n\nThe LORD is my shepherd; I shall not want."
        "📖 <b>Philippians 4:13 (KJV)</b>\n\nI can do all things through Christ which strengtheneth me."
        "📖 <b>Jeremiah 29:11 (KJV)</b>\n\nFor I know the thoughts that I think toward you, saith the LORD, thoughts of peace, and not of evil, to give you an expected end."
        "📖 <b>Romans 8:28 (KJV)</b>\n\nAnd we know that all things work together for good to them that love God, to them who are the called according to his purpose."
        "📖 <b>Proverbs 3:5-6 (KJV)</b>\n\nTrust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths."
        "📖 <b>Isaiah 40:31 (KJV)</b>\n\nBut they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint."
        "📖 <b>Matthew 28:19-20 (KJV)</b>\n\nGo ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost: Teaching them to observe all things whatsoever I have commanded you: and, lo, I am with you alway, even unto the end of the world."
        "📖 <b>Galatians 5:22-23 (KJV)</b>\n\nBut the fruit of the Spirit is love, joy, peace, longsuffering, gentleness, goodness, faith, Meekness, temperance: against such there is no law."
        "📖 <b>Joshua 1:9 (KJV)</b>\n\nHave not I commanded thee? Be strong and of a good courage; be not afraid, neither be thou dismayed: for the LORD thy God is with thee whithersoever thou goest."
        "📖 <b>Psalm 119:105 (KJV)</b>\n\nThy word is a lamp unto my feet, and a light unto my path."
        "📖 <b>2 Timothy 3:16 (KJV)</b>\n\nAll scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness."
        "📖 <b>1 Corinthians 13:4-7 (KJV)</b>\n\nCharity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up, Doth not behave itself unseemly, seeketh not her own, is not easily provoked, thinketh no evil; Rejoiceth not in iniquity, but rejoiceth in the truth; Beareth all things, believeth all things, hopeth all things, endureth all things."
        "📖 <b>Ephesians 2:8-9 (KJV)</b>\n\nFor by grace are ye saved through faith; and that not of yourselves: it is the gift of God: Not of works, lest any man should boast."
        "📖 <b>Colossians 3:23 (KJV)</b>\n\nAnd whatsoever ye do, do it heartily, as to the Lord, and not unto men."
        "📖 <b>James 1:5 (KJV)</b>\n\nIf any of you lack wisdom, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him."
        "📖 <b>1 Peter 5:7 (KJV)</b>\n\nCasting all your care upon him; for he careth for you."
        "📖 <b>1 John 4:7-8 (KJV)</b>\n\nBeloved, let us love one another: for love is of God; and every one that loveth is born of God, and knoweth God. He that loveth not knoweth not God; for God is love."
        "📖 <b>Revelation 3:20 (KJV)</b>\n\nBehold, I stand at the door, and knock: if any man hear my voice, and open the door, I will come in to him, and will sup with him, and he with me."
        "📖 <b>Genesis 1:1 (KJV)</b>\n\nIn the beginning God created the heaven and the earth."
    )
    
    # Get random verse
    local random_index=$((RANDOM % ${#verses[@]}))
    echo "${verses[$random_index]}"
}

# Function to send daily verse to all groups
send_daily_verse() {
    log "🚀 Starting daily verse distribution..."
    
    # Get a random verse
    local verse=$(get_random_verse)
    log "📖 Selected verse: ${verse:0:50}..."
    
    # Split chat IDs by comma
    IFS=',' read -ra CHAT_ARRAY <<< "$TELEGRAM_CHAT_IDS"
    
    local success_count=0
    local total_count=${#CHAT_ARRAY[@]}
    
    # Send verse to each chat
    for chat_id in "${CHAT_ARRAY[@]}"; do
        chat_id=$(echo "$chat_id" | tr -d ' ')  # Remove whitespace
        
        if [ -n "$chat_id" ]; then
            log "📱 Sending verse to chat: $chat_id"
            
            if send_verse_to_chat "$chat_id" "$verse"; then
                ((success_count++))
            fi
            
            # Small delay between sends to avoid rate limiting
            sleep 1
        fi
    done
    
    log "🎯 Verse distribution completed: $success_count/$total_count successful"
    
    # Add timestamp footer
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local footer="\n\n<i>📅 Sent on $timestamp</i>"
    
    # Send footer to each chat
    for chat_id in "${CHAT_ARRAY[@]}"; do
        chat_id=$(echo "$chat_id" | tr -d ' ')
        if [ -n "$chat_id" ]; then
            send_verse_to_chat "$chat_id" "$footer" || true
            sleep 0.5
        fi
    done
}

# Function to send a test verse
send_test_verse() {
    log "🧪 Sending test verse..."
    
    local test_verse="🧪 <b>Test Message</b>\n\nThis is a test message to verify the bot is working correctly.\n\nIf you see this, the bot is functioning properly! ✅"
    
    # Split chat IDs by comma
    IFS=',' read -ra CHAT_ARRAY <<< "$TELEGRAM_CHAT_IDS"
    
    for chat_id in "${CHAT_ARRAY[@]}"; do
        chat_id=$(echo "$chat_id" | tr -d ' ')
        if [ -n "$chat_id" ]; then
            log "📱 Sending test to chat: $chat_id"
            send_verse_to_chat "$chat_id" "$test_verse" || true
            sleep 0.5
        fi
    done
    
    log "✅ Test verse sent to all groups"
}

# Function to show help
show_help() {
    echo "Bible Verse Bot - Bash Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  --test     Send a test verse to all groups"
    echo "  --verse    Send a daily verse to all groups"
    echo "  --help     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --test     # Send test message"
    echo "  $0 --verse    # Send daily verse"
    echo ""
    echo "For scheduled sending, add to crontab:"
    echo "  0 7,12,19 * * * $SCRIPT_DIR/send_verses.sh --verse"
    echo ""
    echo "Or use systemd timer (see scripts/setup_systemd.sh)"
}

# Main script logic
case "${1:---verse}" in
    --test)
        send_test_verse
        ;;
    --verse)
        send_daily_verse
        ;;
    --help|-h)
        show_help
        ;;
    *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
esac 