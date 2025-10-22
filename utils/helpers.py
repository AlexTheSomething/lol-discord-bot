"""
Helper functions for formatting data and creating Discord embeds.
"""

import discord
from typing import Dict, Any, Optional
from datetime import datetime
import config


def format_rank(rank_data: Dict[str, Any]) -> str:
    """
    Format rank data into a readable string.
    
    Args:
        rank_data: Rank data from Riot API
        
    Returns:
        Formatted rank string (e.g., "Gold II - 45 LP")
    """
    tier = rank_data.get("tier", "Unranked").capitalize()
    rank = rank_data.get("rank", "")
    lp = rank_data.get("leaguePoints", 0)
    
    if tier == "Unranked":
        return "Unranked"
    
    return f"{tier} {rank} - {lp} LP"


def calculate_winrate(wins: int, losses: int) -> float:
    """
    Calculate winrate percentage.
    
    Args:
        wins: Number of wins
        losses: Number of losses
        
    Returns:
        Winrate as a percentage (0-100)
    """
    total_games = wins + losses
    if total_games == 0:
        return 0.0
    return round((wins / total_games) * 100, 1)


def format_kda(kills: int, deaths: int, assists: int) -> str:
    """
    Format KDA into a readable string.
    
    Args:
        kills: Number of kills
        deaths: Number of deaths
        assists: Number of assists
        
    Returns:
        Formatted KDA string (e.g., "5/3/7")
    """
    return f"{kills}/{deaths}/{assists}"


def calculate_kda_ratio(kills: int, deaths: int, assists: int) -> float:
    """
    Calculate KDA ratio.
    
    Args:
        kills: Number of kills
        deaths: Number of deaths
        assists: Number of assists
        
    Returns:
        KDA ratio
    """
    if deaths == 0:
        return float(kills + assists)
    return round((kills + assists) / deaths, 2)


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to MM:SS format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "25:43")
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def format_timestamp(timestamp_ms: int) -> str:
    """
    Format Unix timestamp (milliseconds) to readable date.
    
    Args:
        timestamp_ms: Unix timestamp in milliseconds
        
    Returns:
        Formatted date string
    """
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return dt.strftime("%Y-%m-%d %H:%M")


def get_profile_icon_url(icon_id: int) -> str:
    """
    Get profile icon URL from Data Dragon.
    
    Args:
        icon_id: Profile icon ID
        
    Returns:
        Full URL to profile icon image
    """
    return f"{config.DDRAGON_BASE_URL}/img/profileicon/{icon_id}.png"


def get_champion_icon_url(champion_name: str) -> str:
    """
    Get champion icon URL from Data Dragon.
    
    Args:
        champion_name: Champion name
        
    Returns:
        Full URL to champion icon image
    """
    return f"{config.DDRAGON_BASE_URL}/img/champion/{champion_name}.png"


def create_basic_embed(title: str, description: str = "", color: int = config.EMBED_COLOR) -> discord.Embed:
    """
    Create a basic Discord embed with standard formatting.
    
    Args:
        title: Embed title
        description: Embed description
        color: Embed color (hex)
        
    Returns:
        Discord Embed object
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    embed.set_footer(text="League of Legends Bot")
    return embed


def create_error_embed(error_message: str) -> discord.Embed:
    """
    Create an error embed with red color.
    
    Args:
        error_message: Error message to display
        
    Returns:
        Discord Embed object
    """
    embed = discord.Embed(
        title="❌ Error",
        description=error_message,
        color=0xFF0000,
        timestamp=datetime.now()
    )
    embed.set_footer(text="League of Legends Bot")
    return embed


def create_summoner_embed(summoner_data: Dict[str, Any]) -> discord.Embed:
    """
    Create an embed for summoner information.
    
    Args:
        summoner_data: Summoner data from Riot API
        
    Returns:
        Discord Embed object
    """
    game_name = summoner_data.get("gameName", "Unknown")
    tag_line = summoner_data.get("tagLine", "Unknown")
    level = summoner_data.get("summonerLevel", "N/A")
    region = summoner_data.get("region", "N/A").upper()
    icon_id = summoner_data.get("profileIconId", 0)
    
    embed = create_basic_embed(
        title=f"{game_name}#{tag_line}",
        description=f"Region: {region}"
    )
    embed.add_field(name="Level", value=str(level), inline=True)
    embed.set_thumbnail(url=get_profile_icon_url(icon_id))
    
    return embed


def create_rank_embed(summoner_data: Dict[str, Any], rank_data: list) -> discord.Embed:
    """
    Create an embed for ranked information.
    
    Args:
        summoner_data: Summoner data from Riot API
        rank_data: List of ranked queue data
        
    Returns:
        Discord Embed object
    """
    game_name = summoner_data.get("gameName", "Unknown")
    tag_line = summoner_data.get("tagLine", "Unknown")
    
    embed = create_basic_embed(
        title=f"Ranked Stats - {game_name}#{tag_line}"
    )
    
    if not rank_data:
        embed.description = "No ranked data available (Unranked)"
        return embed
    
    # Find Solo/Duo and Flex queue data
    solo_data = None
    flex_data = None
    
    for queue in rank_data:
        if queue.get("queueType") == "RANKED_SOLO_5x5":
            solo_data = queue
        elif queue.get("queueType") == "RANKED_FLEX_SR":
            flex_data = queue
    
    # Add Solo/Duo field
    if solo_data:
        rank_str = format_rank(solo_data)
        wins = solo_data.get("wins", 0)
        losses = solo_data.get("losses", 0)
        winrate = calculate_winrate(wins, losses)
        
        embed.add_field(
            name="🏆 Ranked Solo/Duo",
            value=f"**{rank_str}**\n{wins}W {losses}L ({winrate}%)",
            inline=False
        )
    else:
        embed.add_field(name="🏆 Ranked Solo/Duo", value="Unranked", inline=False)
    
    # Add Flex field
    if flex_data:
        rank_str = format_rank(flex_data)
        wins = flex_data.get("wins", 0)
        losses = flex_data.get("losses", 0)
        winrate = calculate_winrate(wins, losses)
        
        embed.add_field(
            name="👥 Ranked Flex",
            value=f"**{rank_str}**\n{wins}W {losses}L ({winrate}%)",
            inline=False
        )
    else:
        embed.add_field(name="👥 Ranked Flex", value="Unranked", inline=False)
    
    return embed


def get_region_choices() -> list:
    """
    Get list of region choices for Discord slash command parameters.
    
    Returns:
        List of discord.app_commands.Choice objects
    """
    regions = [
        ("EUN (EU Nordic & East)", "eun1"),
        ("EUW (EU West)", "euw1"),
        ("NA (North America)", "na1"),
        ("BR (Brazil)", "br1"),
        ("LAN (Latin America North)", "la1"),
        ("LAS (Latin America South)", "la2"),
        ("OCE (Oceania)", "oc1"),
        ("KR (Korea)", "kr"),
        ("JP (Japan)", "jp1"),
        ("TR (Turkey)", "tr1"),
        ("RU (Russia)", "ru"),
    ]
    
    return [discord.app_commands.Choice(name=name, value=value) for name, value in regions]

