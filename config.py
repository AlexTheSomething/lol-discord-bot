"""
Configuration file for the Discord Riot Bot.
Loads environment variables and defines region mappings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "your_discord_token_here")

# Riot Games API Key
RIOT_API_KEY = os.getenv("RIOT_API_KEY", "your_riot_api_key_here")

# Default region for Riot API requests
DEFAULT_REGION = "eun1"

# Platform routing endpoints (for summoner, ranked, mastery, spectator endpoints)
PLATFORM_ROUTING = {
    "br1": "https://br1.api.riotgames.com",
    "eun1": "https://eun1.api.riotgames.com",
    "euw1": "https://euw1.api.riotgames.com",
    "jp1": "https://jp1.api.riotgames.com",
    "kr": "https://kr.api.riotgames.com",
    "la1": "https://la1.api.riotgames.com",
    "la2": "https://la2.api.riotgames.com",
    "na1": "https://na1.api.riotgames.com",
    "oc1": "https://oc1.api.riotgames.com",
    "tr1": "https://tr1.api.riotgames.com",
    "ru": "https://ru.api.riotgames.com",
    "ph2": "https://ph2.api.riotgames.com",
    "sg2": "https://sg2.api.riotgames.com",
    "th2": "https://th2.api.riotgames.com",
    "tw2": "https://tw2.api.riotgames.com",
    "vn2": "https://vn2.api.riotgames.com",
}

# Regional routing endpoints (for match history and tournament data)
REGIONAL_ROUTING = {
    "br1": "https://americas.api.riotgames.com",
    "eun1": "https://europe.api.riotgames.com",
    "euw1": "https://europe.api.riotgames.com",
    "jp1": "https://asia.api.riotgames.com",
    "kr": "https://asia.api.riotgames.com",
    "la1": "https://americas.api.riotgames.com",
    "la2": "https://americas.api.riotgames.com",
    "na1": "https://americas.api.riotgames.com",
    "oc1": "https://sea.api.riotgames.com",
    "tr1": "https://europe.api.riotgames.com",
    "ru": "https://europe.api.riotgames.com",
    "ph2": "https://sea.api.riotgames.com",
    "sg2": "https://sea.api.riotgames.com",
    "th2": "https://sea.api.riotgames.com",
    "tw2": "https://sea.api.riotgames.com",
    "vn2": "https://sea.api.riotgames.com",
}

# Data Dragon version (for champion icons, etc.)
DDRAGON_VERSION = "14.1.1"
DDRAGON_BASE_URL = f"https://ddragon.leagueoflegends.com/cdn/{DDRAGON_VERSION}"

# League of Legends branding color for embeds
EMBED_COLOR = 0x0397AB  # Riot Games blue

