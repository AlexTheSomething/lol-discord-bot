# 🚀 Bot Hosting Guide

## Pre-Hosting Checklist

Before deploying your bot to a 24/7 hosting service, complete these steps:

### ✅ **1. API Key Type**

- [ ] **Switch to Personal/Production API Key** (Development keys expire every 24 hours!)
  - Go to: https://developer.riotgames.com/
  - Register your product if you haven't already
  - Use the personal API key instead of development key

### ✅ **2. Test All Commands**

Run through each command to ensure everything works:

- [ ] `/summoner` - Test with multiple players
- [ ] `/rank` - Verify rank data shows correctly
- [ ] `/recentmatches` - Check match history
- [ ] `/championmastery` - Verify champion data
- [ ] `/rotation` - Check free rotation
- [ ] `/livegame` - Test during an active game
- [ ] `/compare` - Compare two players
- [ ] `/randomchampion` - Get random suggestions
- [ ] `/build` - Check build links
- [ ] `/ping` - Verify latency
- [ ] `/help` - Review command list
- [ ] `/about` - Check bot info

### ✅ **3. Test Stalking System**

- [ ] `/stalk set` - Set a tracking channel
- [ ] `/stalk add` - Add 2-3 test players
- [ ] `/stalk list` - Verify players appear
- [ ] Wait 2-5 minutes - Check if monitoring detects matches
- [ ] Verify thread updates work correctly
- [ ] Test duo detection (if players play together)
- [ ] `/stalk remove` - Remove a test player
- [ ] Verify thread gets archived

### ✅ **4. Error Handling**

Test edge cases:

- [ ] Try commands with invalid player names
- [ ] Try commands with wrong regions
- [ ] Test with unranked accounts
- [ ] Test with brand new accounts
- [ ] Try stalking a player that doesn't exist

### ✅ **5. Performance Check**

- [ ] Monitor console for errors during 1-hour test run
- [ ] Check if monitoring loop runs smoothly every 2 minutes
- [ ] Verify no memory leaks (watch task manager)
- [ ] Test with 5-10 stalked players simultaneously

### ✅ **6. Security Audit**

- [ ] **Verify `.env` is in `.gitignore`** (CRITICAL!)
- [ ] Check GitHub repo - ensure `.env` is NOT visible
- [ ] Confirm API keys are not hardcoded anywhere
- [ ] Review permissions - bot only has what it needs

### ✅ **7. Code Cleanup**

- [ ] Remove any debug `print()` statements (or keep important ones)
- [ ] Check for any `# TODO` comments
- [ ] Verify all error messages are user-friendly
- [ ] Ensure all docstrings are accurate

### ✅ **8. Documentation**

- [ ] Update README with any final changes
- [ ] Verify installation instructions work
- [ ] Test setup from scratch on another machine (optional)
- [ ] Push final version to GitHub

---

## 🌐 Hosting Options

### **Option 1: PebbleHost / BisectHosting (Cheap & Easy)**

**Best for:** Beginners, small servers (< 100 tracked players)

**Pros:**
- ✅ Cheap ($1-5/month)
- ✅ Easy setup
- ✅ 24/7 uptime
- ✅ Support for Python bots

**Cons:**
- ❌ Limited resources
- ❌ Shared hosting (can be slow)

**Setup:**
1. Purchase Python bot hosting
2. Upload your bot files via FTP/SFTP
3. Install requirements: `pip install -r requirements.txt`
4. Set environment variables in control panel
5. Start bot from control panel

---

### **Option 2: Railway.app / Render.com (Free Tier Available)**

**Best for:** Medium usage, good for testing 24/7 hosting

**Pros:**
- ✅ Free tier available
- ✅ Easy GitHub integration
- ✅ Automatic deploys from GitHub
- ✅ Environment variable management
- ✅ Better performance than budget hosting

**Cons:**
- ❌ Free tier has limits (500 hours/month on Railway)
- ❌ May sleep after inactivity (on free tier)

**Setup (Railway.app):**
1. Sign up at https://railway.app/
2. "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variables:
   - `DISCORD_TOKEN`
   - `RIOT_API_KEY`
5. Railway auto-detects Python and installs dependencies
6. Bot starts automatically!

---

### **Option 3: DigitalOcean / AWS / GCP (Advanced)**

**Best for:** Large servers, advanced users, full control

**Pros:**
- ✅ Full control over server
- ✅ Scalable resources
- ✅ Professional-grade hosting
- ✅ Can host multiple bots

**Cons:**
- ❌ More expensive ($5-50+/month)
- ❌ Requires Linux/server knowledge
- ❌ Manual setup required

**Setup (DigitalOcean Droplet):**
1. Create $5/month droplet (Ubuntu 22.04)
2. SSH into server
3. Install Python 3.10+
4. Clone your GitHub repo
5. Create `.env` file with your tokens
6. Install dependencies: `pip install -r requirements.txt`
7. Set up systemd service for auto-restart
8. Run bot: `python bot.py`

---

### **Option 4: Replit (Quick Testing)**

**Best for:** Quick testing, temporary hosting

**Pros:**
- ✅ Free tier available
- ✅ Super easy setup
- ✅ In-browser IDE

**Cons:**
- ❌ Bot sleeps when inactive (free tier)
- ❌ Requires "always on" hack or paid tier
- ❌ Limited resources

---

## 🎯 **Recommended Setup for Your Bot**

Based on your bot's features:

1. **If testing/learning:** Start with **Replit** or **Railway.app** (free tier)
2. **If serious but small server:** **Railway.app** ($5/month) or **PebbleHost**
3. **If large server (100+ tracked players):** **DigitalOcean Droplet** ($5-10/month)

---

## 🛠️ **Additional Production Features (Optional)**

### **1. Logging System**

Add proper logging instead of `print()` statements:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

### **2. Restart on Crash**

If hosting manually, use a process manager:

**Option A: Systemd (Linux)**
```ini
# /etc/systemd/system/lolbot.service
[Unit]
Description=LoL Discord Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Option B: PM2 (Cross-platform)**
```bash
npm install -g pm2
pm2 start bot.py --interpreter python3 --name lolbot
pm2 startup  # Enable auto-start on boot
pm2 save
```

### **3. Rate Limit Handling**

Your bot already handles this gracefully, but monitor for rate limit errors in production.

### **4. Database (Advanced)**

For larger deployments, consider migrating from JSON to SQLite/PostgreSQL:
- Faster reads/writes
- Better data integrity
- Scales better with many tracked players

---

## 📊 **Expected Resource Usage**

- **RAM:** ~100-200 MB (depends on stalked players)
- **CPU:** Very low (< 5% on average)
- **Network:** ~10-50 MB/day (depends on API calls)
- **Storage:** < 50 MB (bot + dependencies + data)

**With 10 stalked players:**
- Monitoring every 2 minutes = 30 checks/hour
- ~1-3 API calls per check = 30-90 calls/hour
- Well within Riot API limits!

---

## 🚨 **Important Notes**

1. **API Key Security:**
   - NEVER commit `.env` to GitHub
   - Rotate API key if accidentally exposed
   - Use environment variables on hosting platform

2. **Monitoring:**
   - Check bot status daily for first week
   - Set up Discord notifications for crashes (optional)
   - Monitor API rate limits

3. **Backups:**
   - Hosting platform should back up `data/tracked_users.json`
   - Or set up automatic GitHub commits for data (advanced)

4. **Updates:**
   - Test updates locally first
   - Keep GitHub repo updated
   - Redeploy from GitHub when hosting

---

## 🎉 **Ready to Host?**

Once you've completed the checklist above, choose a hosting option and deploy!

**Need help with a specific hosting platform?** Check their documentation or ask in their support channels.

**Your bot is production-ready!** 🚀

