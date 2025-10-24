# League of Legends Discord Bot 👁️

A Discord bot that integrates with the Riot Games API to provide League of Legends player statistics and real-time match monitoring through Discord threads!

## ✨ Features

### ✅ Features:
- **Summoner Information** - View player level, region, and profile icon
- **Ranked Stats** - View ranked data, LP, and winrate
- **Match History** - Show recent matches with KDA and results
- **Champion Mastery** - View top champions by mastery points
- **Free Rotation** - Check current free champion rotation
- **Live Game Detection** - See if a player is currently in game
- **Player Tracking** - Track players in dedicated Discord threads (stalking board)
- **Real-Time Monitoring** - Automatically detects new matches every 2 minutes
- **Duo Detection** - Tracks who players team up with repeatedly
- **Comparison** - Compare two summoners side by side
- **Champion Builds** - Get links to popular build resources
- **Random Champion** - Get a random champion suggestion

## 📋 Prerequisites

- Python 3.10 or higher
- A Discord Bot Token
- A Riot Games API Key

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/discord-riot-bot.git
cd discord-riot-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Your Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under the "Token" section, click "Copy" to copy your bot token
6. **Enable the following Privileged Gateway Intents:**
   - Presence Intent
   - Server Members Intent
   - Message Content Intent

7. Go to "OAuth2" → "URL Generator"
8. Select scopes: `bot` and `applications.commands`
9. Select bot permissions:
   - **Text Permissions:**
     - `Send Messages`
     - `Send Messages in Threads`
     - `Create Public Threads`
     - `Manage Threads` (for archiving tracked players)
     - `Embed Links`
     - `Read Message History`
     - `Use Slash Commands`
10. Copy the generated URL and use it to invite the bot to your server

### 4. Get Your Riot Games API Key

1. Go to the [Riot Developer Portal](https://developer.riotgames.com/)
2. Sign in with your Riot Games account
3. Click "REGISTER PRODUCT" or navigate to your dashboard
4. For development, you can use the "Development API Key" (regenerates every 24 hours)
5. For production, you'll need to apply for a "Production API Key"
6. Copy your API key

### 5. Configure Environment Variables

Create a `.env` file in the root directory (or rename the existing one):

```env
DISCORD_TOKEN=your_discord_token_here
RIOT_API_KEY=your_riot_api_key_here
```

Replace `your_discord_token_here` with your Discord bot token and `your_riot_api_key_here` with your Riot API key.

### 6. Configure Default Region (Optional)

Edit `config.py` to change the default region:

```python
DEFAULT_REGION = "eun1"  # Change this to your preferred region
```

## ▶️ Running the Bot

```bash
python bot.py
```

You should see output indicating the bot is loading commands and connecting to Discord:

```
Loading commands...
✓ Loaded command: summoner
✓ Loaded command: rank
...
Syncing commands with Discord...
Commands synced successfully!

==================================================
Bot is online and ready!
Logged in as: YourBotName (ID: 123456789)
==================================================
```

## 📝 Available Commands

### Data Display Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/summoner` | Display summoner information | `/summoner game_name:PlayerName tag_line:TAG` |
| `/rank` | Show ranked stats and winrate | `/rank game_name:PlayerName tag_line:TAG` |
| `/recentmatches` | Display last 5 matches | `/recentmatches game_name:PlayerName tag_line:TAG` |
| `/championmastery` | Show top 5 champions | `/championmastery game_name:PlayerName tag_line:TAG` |
| `/rotation` | Current free champion rotation | `/rotation` |
| `/livegame` | Show current match if in game | `/livegame game_name:PlayerName tag_line:TAG` |

### Stalking Commands (Thread-Based)

| Command | Description | Usage |
|---------|-------------|-------|
| `/stalk set` | Set the stalking channel | `/stalk set channel:#your-channel` |
| `/stalk unset` | Remove stalking channel | `/stalk unset` |
| `/stalk add` | Stalk a player (creates thread) | `/stalk add game_name:PlayerName tag_line:TAG` |
| `/stalk list` | List all stalked players | `/stalk list` |
| `/stalk remove` | Stop stalking a player | `/stalk remove game_name:PlayerName tag_line:TAG` |
| `/compare` | Compare two summoners | `/compare game_name1:Player1 tag_line1:TAG1 game_name2:Player2 tag_line2:TAG2` |

### Utility Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/randomchampion` | Random champion suggestion | `/randomchampion [from_rotation:True/False]` |
| `/build` | Get build resources | `/build champion_name:Ahri` |
| `/clash` | Show upcoming Clash tournaments | `/clash` |
| `/ping` | Check bot latency | `/ping` |
| `/help` | Show all commands | `/help` |
| `/about` | Bot information | `/about` |

## 🌍 Region Configuration

The bot uses a **default region** set in `config.py`. Change it to match your server's region:

```python
DEFAULT_REGION = "eun1"  # Change to your preferred region
```

**Supported regions:**
`eun1`, `euw1`, `na1`, `br1`, `la1`, `la2`, `oc1`, `kr`, `jp1`, `tr1`, `ru`

## 🔑 Riot ID Format

Riot Games now uses the **Riot ID** format for player identification:

- Format: `GameName#TAG`
- Example: `Faker#KR1`
- When using commands, separate the game name and tag:
  - `game_name: Faker`
  - `tag_line: KR1`

## 👁️ Real-Time Player Tracking System

The bot features a unique **automated thread-based tracking system**:

### Setup:
1. **Set up the tracking channel:**
   ```
   /stalk set channel:#player-tracking
   ```
   Works with both forum channels and text channels!

2. **Add players to track:**
   ```
   /stalk add game_name:Faker tag_line:KR1
   ```
   - Creates a dedicated thread "👁️ Faker#KR1"
   - Posts their current stats
   - **Automatically monitors them every 2 minutes!**

3. **View all tracked players:**
   ```
   /stalk list
   ```

4. **Remove a player:**
   ```
   /stalk remove game_name:Faker tag_line:KR1
   ```

### Automatic Monitoring:
Once tracked, the bot automatically (every 2 minutes):
- ✅ Detects when they start/finish matches
- ✅ Posts match results with KDA to their thread
- ✅ **Tracks LP gains/losses** (e.g., "Silver IV 45 LP → 62 LP (+17) 📈")
- ✅ **Alerts on promotions/demotions** (e.g., "🎉 PROMOTION! Silver III!")
- ✅ Tracks who they play with (duo detection)
- ✅ Shows recurring teammates (3+ games together)

**Perfect for:** Tracking pro players, monitoring friends, or keeping tabs on rivals! 👁️

## 📁 Project Structure

```
discord-riot-bot/
├── bot.py                  # Main bot file
├── config.py              # Configuration and API keys
├── riot_api.py            # Riot API handler
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── README.md              # This file
├── commands/              # Slash commands
│   ├── summoner.py
│   ├── rank.py
│   ├── recentmatches.py
│   ├── championmastery.py
│   ├── rotation.py
│   ├── livegame.py
│   ├── track.py          # Thread-based tracking system
│   ├── compare.py
│   ├── randomchampion.py
│   ├── build.py
│   ├── ping.py
│   ├── help.py
│   └── about.py
├── data/                  # Data storage
│   └── tracked_users.json
└── utils/                 # Helper functions
    └── helpers.py
```

## 🛠️ Troubleshooting

### Bot doesn't respond to slash commands

1. Make sure you've invited the bot with the `applications.commands` scope
2. Wait a few minutes for Discord to sync the commands globally
3. Try kicking and re-inviting the bot
4. Check that the bot has proper permissions in your server

### Tracking commands not working

1. Make sure the bot has these permissions in your tracking channel:
   - Send Messages
   - Create Public Threads (for text channels)
   - Send Messages in Threads
   - Manage Threads
2. Use `/stalk set` to set a valid forum or text channel
3. Check that the channel still exists (wasn't deleted)

### "Invalid API key" error

- Make sure you've correctly copied your Riot API key to the `.env` file
- **Development API keys expire after 24 hours** - You'll need to regenerate daily
- **Personal/Production API keys don't expire** - Recommended for 24/7 hosting
- Ensure there are no extra spaces in your `.env` file

### "Rate limit exceeded" error

- The personal API key allows 20 requests/second and 100 requests/2 minutes
- If you're testing heavily, wait a minute before trying again
- Consider implementing request caching for production use

### "Player or data not found" error

- Verify the Riot ID format (GameName#TAG)
- Make sure you're using the correct region
- Check that the summoner name is spelled correctly
- Some new accounts may not have ranked data

### Bot won't start

- Verify Python version is 3.10 or higher: `python --version`
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that your Discord token is valid
- Look for error messages in the console output

## 📜 License

This project is open source and available for educational purposes. 

**Legal Notice:** This project is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [Riot API Documentation](https://developer.riotgames.com/docs/lol)
3. Check the [Discord.py Documentation](https://discordpy.readthedocs.io/)

## 🙏 Acknowledgments

- [Riot Games](https://www.riotgames.com/) for providing the API
- [Discord.py](https://github.com/Rapptz/discord.py) for the Discord library
- The League of Legends community

---

**Enjoy using the bot! 🎮**

