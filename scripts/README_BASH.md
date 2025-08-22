# 📖 Bible Verse Bot - Bash Script Version

A lightweight, reliable alternative to the Python bot that sends Bible verses to Telegram groups using bash scripts and systemd timers.

## 🚀 **Why Bash Scripts?**

- **Lightweight** - No Python dependencies or virtual environments
- **Reliable** - Uses systemd timers (more reliable than cron)
- **Simple** - Easy to understand and modify
- **Efficient** - Minimal resource usage
- **Native** - Works directly with system scheduling

## 📁 **Files**

- **`send_verses.sh`** - Main script that sends verses
- **`setup_systemd.sh`** - Sets up automated scheduling
- **`README_BASH.md`** - This documentation

## ⚙️ **Setup**

### **1. Make Scripts Executable**

```bash
chmod +x scripts/send_verses.sh scripts/setup_systemd.sh
```

### **2. Test the Script**

```bash
./scripts/send_verses.sh --test
```

### **3. Setup Automated Scheduling**

```bash
# Option 1: Systemd timer (recommended)
./scripts/setup_systemd.sh --systemd

# Option 2: Crontab
./scripts/setup_systemd.sh --crontab

# Option 3: Both
./scripts/setup_systemd.sh --both
```

## 🕐 **Scheduled Times**

The bot is configured to send verses at:

- **07:00** - Morning verse
- **12:30** - Midday verse  
- **19:00** - Evening verse

All times are in your local timezone (Africa/Addis_Ababa).

## 📖 **Verse Selection**

The bash script includes **20 carefully selected Bible verses** from the KJV translation:

- John 3:16, Psalm 23:1, Philippians 4:13
- Jeremiah 29:11, Romans 8:28, Proverbs 3:5-6
- Isaiah 40:31, Matthew 28:19-20, Galatians 5:22-23
- Joshua 1:9, Psalm 119:105, 2 Timothy 3:16
- 1 Corinthians 13:4-7, Ephesians 2:8-9, Colossians 3:23
- James 1:5, 1 Peter 5:7, 1 John 4:7-8, Revelation 3:20

## 🔧 **Usage**

### **Manual Sending**

```bash
# Send a test verse
./scripts/send_verses.sh --test

# Send a daily verse
./scripts/send_verses.sh --verse

# Show help
./scripts/send_verses.sh --help
```

### **Check Status**

```bash
# Check systemd timer status
./scripts/setup_systemd.sh --status

# View systemd logs
journalctl --user -u bible-verse-bot.service

# View crontab logs (if using crontab)
tail -f data/logs/cron.log
```

## 🛠️ **Customization**

### **Change Scheduled Times**

Edit the timer file:

```bash
nano ~/.config/systemd/user/bible-verse-bot.timer
```

Or modify the setup script and re-run it.

### **Add More Verses**

Edit `send_verses.sh` and add more verses to the `verses` array.

### **Change Translation**

Modify the verse text in the script to use different translations.

## 🔍 **Troubleshooting**

### **Script Not Running**

1. Check if systemd timer is active:

   ```bash
   systemctl --user status bible-verse-bot.timer
   ```

2. Check logs:

   ```bash
   journalctl --user -u bible-verse-bot.service
   ```

3. Test manual execution:

   ```bash
   ./scripts/send_verses.sh --test
   ```

### **Permission Issues**

1. Make sure scripts are executable:

   ```bash
   chmod +x scripts/*.sh
   ```

2. Check .env file permissions:

   ```bash
   ls -la .env
   ```

### **Systemd Issues**

1. Reload systemd:

   ```bash
   systemctl --user daemon-reload
   ```

2. Restart timer:

   ```bash
   systemctl --user restart bible-verse-bot.timer
   ```

## 📊 **Monitoring**

### **Check Timer Status**

```bash
systemctl --user list-timers
```

### **View Recent Activity**

```bash
journalctl --user -u bible-verse-bot.service --since "1 hour ago"
```

### **Check Crontab (if using)**

```bash
crontab -l
```

## 🔄 **Switching from Python Bot**

If you want to use the bash script instead of the Python bot:

1. **Stop the Python bot:**

   ```bash
   pkill -f "python.*main.py"
   ```

2. **Setup bash script scheduling:**

   ```bash
   ./scripts/setup_systemd.sh --systemd
   ```

3. **Test the setup:**

   ```bash
   ./scripts/send_verses.sh --test
   ```

## 🎯 **Benefits of Bash Version**

- ✅ **No Python dependencies**
- ✅ **Systemd integration**
- ✅ **Lightweight and fast**
- ✅ **Easy to customize**
- ✅ **Reliable scheduling**
- ✅ **Simple logging**
- ✅ **Resource efficient**

## 🆚 **Python vs Bash**

| Feature | Python Bot | Bash Script |
|---------|------------|-------------|
| **Dependencies** | Python + packages | None |
| **Setup** | Virtual environment | Simple scripts |
| **Scheduling** | Built-in scheduler | Systemd/cron |
| **Randomization** | Full Bible API | 20 selected verses |
| **Translations** | 7 versions | KJV only |
| **Resource Usage** | Higher | Minimal |
| **Maintenance** | More complex | Simple |

## 🚀 **Quick Start Summary**

```bash
# 1. Make executable
chmod +x scripts/*.sh

# 2. Test
./scripts/send_verses.sh --test

# 3. Setup automation
./scripts/setup_systemd.sh --systemd

# 4. Check status
./scripts/setup_systemd.sh --status
```

That's it! Your bot will now automatically send Bible verses at the scheduled times. 🎉
