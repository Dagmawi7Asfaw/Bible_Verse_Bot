#!/bin/bash

# Setup script for systemd timers to run the Bible Verse Bot bash script
# This creates systemd service and timer files for automated verse sending

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
USER=$(whoami)

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

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    error "This script should not be run as root"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    error ".env file not found in $PROJECT_DIR"
    exit 1
fi

# Create systemd service file
create_service_file() {
    local service_file="$HOME/.config/systemd/user/bible-verse-bot.service"
    local service_dir=$(dirname "$service_file")
    
    # Create directory if it doesn't exist
    mkdir -p "$service_dir"
    
    cat > "$service_file" << EOF
[Unit]
Description=Bible Verse Bot - Send Daily Verses
After=network.target

[Service]
Type=oneshot
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$PROJECT_DIR/scripts/send_verses.sh --verse
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF

    log "✅ Created service file: $service_file"
}

# Create systemd timer file
create_timer_file() {
    local timer_file="$HOME/.config/systemd/user/bible-verse-bot.timer"
    
    cat > "$timer_file" << EOF
[Unit]
Description=Run Bible Verse Bot at scheduled times
Requires=bible-verse-bot.service

[Timer]
# Send verses at 07:00, 12:30, and 19:00 (Africa/Addis_Ababa timezone)
OnCalendar=*-*-* 07:00:00
OnCalendar=*-*-* 12:30:00
OnCalendar=*-*-* 19:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

    log "✅ Created timer file: $timer_file"
}

# Create crontab alternative
create_crontab() {
    log "📅 Creating crontab entry..."
    
    # Check if crontab entry already exists
    if crontab -l 2>/dev/null | grep -q "send_verses.sh"; then
        warn "Crontab entry already exists, skipping..."
        return
    fi
    
    # Create temporary crontab file
    local temp_cron=$(mktemp)
    
    # Add existing crontab entries
    crontab -l 2>/dev/null > "$temp_cron"
    
    # Add Bible verse bot entries
    cat >> "$temp_cron" << EOF

# Bible Verse Bot - Send verses at scheduled times
# 07:00, 12:30, 19:00 (Africa/Addis_Ababa timezone)
0 7,12,19 * * * $PROJECT_DIR/scripts/send_verses.sh --verse >> $PROJECT_DIR/data/logs/cron.log 2>&1
EOF

    # Install new crontab
    crontab "$temp_cron"
    rm "$temp_cron"
    
    log "✅ Added crontab entries"
}

# Enable and start systemd services
enable_services() {
    log "🔧 Enabling systemd services..."
    
    # Reload systemd user daemon
    systemctl --user daemon-reload
    
    # Enable the timer
    systemctl --user enable bible-verse-bot.timer
    
    # Start the timer
    systemctl --user start bible-verse-bot.timer
    
    log "✅ Systemd timer enabled and started"
}

# Show status
show_status() {
    log "📊 Checking service status..."
    
    echo ""
    echo "=== Systemd Timer Status ==="
    systemctl --user status bible-verse-bot.timer --no-pager -l
    
    echo ""
    echo "=== Timer List ==="
    systemctl --user list-timers --no-pager
    
    echo ""
    echo "=== Crontab Status ==="
    if crontab -l 2>/dev/null | grep -q "send_verses.sh"; then
        echo "✅ Crontab entries found:"
        crontab -l | grep "send_verses.sh"
    else
        echo "❌ No crontab entries found"
    fi
}

# Show help
show_help() {
    echo "Bible Verse Bot - Systemd Setup Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  --systemd    Setup systemd timer (recommended)"
    echo "  --crontab    Setup crontab entries"
    echo "  --both       Setup both systemd and crontab"
    echo "  --status     Show current status"
    echo "  --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --systemd    # Setup systemd timer only"
    echo "  $0 --crontab    # Setup crontab only"
    echo "  $0 --both       # Setup both methods"
    echo "  $0 --status     # Check current status"
    echo ""
    echo "Note: Systemd timers are more reliable than crontab"
}

# Main script logic
case "${1:---systemd}" in
    --systemd)
        log "🚀 Setting up systemd timer..."
        create_service_file
        create_timer_file
        enable_services
        show_status
        ;;
    --crontab)
        log "📅 Setting up crontab entries..."
        create_crontab
        show_status
        ;;
    --both)
        log "🚀 Setting up both systemd and crontab..."
        create_service_file
        create_timer_file
        enable_services
        create_crontab
        show_status
        ;;
    --status)
        show_status
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

log "🎯 Setup completed successfully!"
echo ""
echo "💡 Next steps:"
echo "  1. Test the bot: $PROJECT_DIR/scripts/send_verses.sh --test"
echo "  2. Check status: $0 --status"
echo "  3. View logs: journalctl --user -u bible-verse-bot.service"
echo ""
echo "🙏 Happy verse sharing!" 