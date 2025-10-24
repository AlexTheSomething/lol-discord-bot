"""
Riot Games API handler for League of Legends data.
Handles all API requests to Riot Games endpoints.
"""

import aiohttp
from typing import Optional, Dict, List, Any
import config


class RiotAPIError(Exception):
    """Custom exception for Riot API errors."""
    pass


async def _make_request(url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Make an async HTTP GET request to the Riot API.
    
    Args:
        url: The full API endpoint URL
        headers: Request headers including API key
        
    Returns:
        JSON response as dictionary or None if error
        
    Raises:
        RiotAPIError: If the API request fails
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    raise RiotAPIError("Player or data not found")
                elif response.status == 403:
                    raise RiotAPIError("Invalid API key or forbidden access")
                elif response.status == 429:
                    raise RiotAPIError("Rate limit exceeded. Please try again later")
                else:
                    raise RiotAPIError(f"API request failed with status {response.status}")
        except aiohttp.ClientError as e:
            raise RiotAPIError(f"Network error: {str(e)}")


async def get_summoner_by_riot_id(game_name: str, tag_line: str, region: str = config.DEFAULT_REGION) -> Dict[str, Any]:
    """
    Fetch summoner data by Riot ID (game_name#tag_line).
    
    Args:
        game_name: The player's in-game name
        tag_line: The player's tag (without #)
        region: Platform region code (e.g., 'eun1', 'na1')
        
    Returns:
        Dictionary containing summoner data (puuid, gameName, tagLine)
        
    Raises:
        RiotAPIError: If the API request fails
    """
    region_lower = region.lower()
    
    # First, get the account data using the Account-V1 endpoint
    regional_url = config.REGIONAL_ROUTING.get(region_lower)
    if not regional_url:
        raise RiotAPIError(f"Invalid region: {region}")
    
    url = f"{regional_url}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": config.RIOT_API_KEY}
    
    account_data = await _make_request(url, headers)
    
    # Then get summoner data using puuid
    platform_url = config.PLATFORM_ROUTING.get(region_lower)
    summoner_url = f"{platform_url}/lol/summoner/v4/summoners/by-puuid/{account_data['puuid']}"
    summoner_data = await _make_request(summoner_url, headers)
    
    # Combine both data sets
    return {
        **account_data,
        **summoner_data,
        "region": region_lower
    }


async def get_summoner_rank(puuid: str, region: str = config.DEFAULT_REGION) -> List[Dict[str, Any]]:
    """
    Fetch ranked data for a summoner.
    
    Args:
        puuid: The player's PUUID
        region: Platform region code
        
    Returns:
        List of ranked queue data (solo/duo, flex, etc.)
        
    Raises:
        RiotAPIError: If the API request fails
    """
    region_lower = region.lower()
    platform_url = config.PLATFORM_ROUTING.get(region_lower)
    if not platform_url:
        raise RiotAPIError(f"Invalid region: {region}")
    
    # Use the new PUUID-based endpoint (no need for summoner ID!)
    url = f"{platform_url}/lol/league/v4/entries/by-puuid/{puuid}"
    headers = {"X-Riot-Token": config.RIOT_API_KEY}
    return await _make_request(url, headers)


async def get_match_history(puuid: str, region: str = config.DEFAULT_REGION, count: int = 5) -> List[str]:
    """
    Fetch recent match IDs for a summoner.
    
    Args:
        puuid: The player's PUUID
        region: Platform region code
        count: Number of matches to fetch (default 5)
        
    Returns:
        List of match IDs
        
    Raises:
        RiotAPIError: If the API request fails
    """
    region_lower = region.lower()
    regional_url = config.REGIONAL_ROUTING.get(region_lower)
    if not regional_url:
        raise RiotAPIError(f"Invalid region: {region}")
    
    url = f"{regional_url}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    headers = {"X-Riot-Token": config.RIOT_API_KEY}
    
    return await _make_request(url, headers)


async def get_match_details(match_id: str, region: str = config.DEFAULT_REGION) -> Dict[str, Any]:
    """
    Fetch detailed information about a specific match.
    
    Args:
        match_id: The match ID
        region: Platform region code
        
    Returns:
        Dictionary containing match details
        
    Raises:
        RiotAPIError: If the API request fails
    """
    region_lower = region.lower()
    regional_url = config.REGIONAL_ROUTING.get(region_lower)
    if not regional_url:
        raise RiotAPIError(f"Invalid region: {region}")
    
    url = f"{regional_url}/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": config.RIOT_API_KEY}
    
    return await _make_request(url, headers)


async def get_champion_mastery(puuid: str, region: str = config.DEFAULT_REGION, count: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch top champion masteries for a summoner.
    
    Args:
        puuid: The player's PUUID
        region: Platform region code
        count: Number of champions to fetch (default 5)
        
    Returns:
        List of champion mastery data
        
    Raises:
        RiotAPIError: If the API request fails
    """
    region_lower = region.lower()
    platform_url = config.PLATFORM_ROUTING.get(region_lower)
    if not platform_url:
        raise RiotAPIError(f"Invalid region: {region}")
    
    url = f"{platform_url}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count={count}"
    headers = {"X-Riot-Token": config.RIOT_API_KEY}
    
    return await _make_request(url, headers)


async def get_champion_rotation(region: str = config.DEFAULT_REGION) -> Dict[str, Any]:
    """
    Fetch current free champion rotation.
    
    Args:
        region: Platform region code
        
    Returns:
        Dictionary containing free champion IDs
        
    Raises:
        RiotAPIError: If the API request fails
    """
    region_lower = region.lower()
    platform_url = config.PLATFORM_ROUTING.get(region_lower)
    if not platform_url:
        raise RiotAPIError(f"Invalid region: {region}")
    
    url = f"{platform_url}/lol/platform/v3/champion-rotations"
    headers = {"X-Riot-Token": config.RIOT_API_KEY}
    
    return await _make_request(url, headers)


async def get_active_game(puuid: str, region: str = config.DEFAULT_REGION) -> Optional[Dict[str, Any]]:
    """
    Fetch current active game for a summoner.
    
    Args:
        puuid: The player's PUUID
        region: Platform region code
        
    Returns:
        Dictionary containing active game data or None if not in game
        
    Raises:
        RiotAPIError: If the API request fails (except 404)
    """
    region_lower = region.lower()
    platform_url = config.PLATFORM_ROUTING.get(region_lower)
    if not platform_url:
        raise RiotAPIError(f"Invalid region: {region}")
    
    # Use the new PUUID-based spectator v5 endpoint
    url = f"{platform_url}/lol/spectator/v5/active-games/by-summoner/{puuid}"
    headers = {"X-Riot-Token": config.RIOT_API_KEY}
    
    try:
        return await _make_request(url, headers)
    except RiotAPIError as e:
        if "not found" in str(e).lower() or "404" in str(e):
            return None  # Player is not in an active game
        raise


async def get_champion_data() -> Dict[str, Any]:
    """
    Fetch champion static data from Data Dragon.
    
    Returns:
        Dictionary containing all champion data
        
    Raises:
        RiotAPIError: If the request fails
    """
    url = f"{config.DDRAGON_BASE_URL}/data/en_US/champion.json"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise RiotAPIError(f"Failed to fetch champion data: {response.status}")
        except aiohttp.ClientError as e:
            raise RiotAPIError(f"Network error fetching champion data: {str(e)}")


def get_champion_name_by_id(champion_id: int, champion_data: Dict[str, Any]) -> str:
    """
    Get champion name from champion ID using Data Dragon data.
    
    Args:
        champion_id: The champion's ID number
        champion_data: Champion data from get_champion_data()
        
    Returns:
        Champion name or "Unknown Champion"
    """
    for champ_name, champ_info in champion_data.get("data", {}).items():
        if int(champ_info.get("key", -1)) == champion_id:
            return champ_info.get("name", "Unknown Champion")
    return "Unknown Champion"


async def get_clash_tournaments(region: str = config.DEFAULT_REGION) -> List[Dict[str, Any]]:
    """
    Fetch upcoming Clash tournament data.
    
    Args:
        region: Region code (e.g., 'na1', 'euw1')
        
    Returns:
        List of clash tournaments
        
    Raises:
        RiotAPIError: If the request fails
    """
    platform_url = config.RIOT_REGIONS.get(region.lower())
    if not platform_url:
        raise RiotAPIError(f"Invalid region: {region}")
    
    url = f"{platform_url}/lol/clash/v1/tournaments"
    headers = {"X-Riot-Token": config.RIOT_API_KEY}
    
    return await _make_request(url, headers) or []

