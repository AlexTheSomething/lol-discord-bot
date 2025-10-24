"""
Track command - Player tracking system using Discord threads.
Creates threads for tracked players in a designated channel.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_basic_embed, create_error_embed, create_summoner_embed, create_rank_embed
import config
import json
import os
from datetime import datetime


# File to store tracking configuration
DATA_FILE = "data/tracked_users.json"


def load_tracking_data():
    """Load tracking configuration from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"tracking_channel_id": None, "tracked_players": []}


def save_tracking_data(data):
    """Save tracking configuration to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    # Create a command group for tracking
    track_group = app_commands.Group(name="stalk", description="Player stalking system")
    
    @track_group.command(name="set", description="Set the stalking channel (forum or text channel)")
    @app_commands.describe(channel="The channel where player threads will be created")
    async def track_set(
        interaction: discord.Interaction,
        channel: discord.TextChannel | discord.ForumChannel
    ):
        """
        Set the parent channel for tracking threads.
        
        Args:
            interaction: Discord interaction
            channel: The channel to use for tracking
        """
        await interaction.response.defer()
        
        try:
            # Check if the bot has permissions in that channel
            permissions = channel.permissions_for(interaction.guild.me)
            
            # For forum channels, we need different permissions
            if isinstance(channel, discord.ForumChannel):
                if not permissions.send_messages:
                    embed = create_error_embed(
                        "I don't have permission to create posts in that forum channel!\n\n"
                        "Required permissions:\n"
                        "• Send Messages (in forum, this allows creating posts)"
                    )
                    await interaction.followup.send(embed=embed)
                    return
            else:  # Text channel
                if not permissions.send_messages or not permissions.create_public_threads:
                    embed = create_error_embed(
                        "I don't have permission to send messages and create threads in that channel!\n\n"
                        "Required permissions:\n"
                        "• Send Messages\n"
                        "• Create Public Threads"
                    )
                    await interaction.followup.send(embed=embed)
                    return
            
            # Save the stalking channel
            data = load_tracking_data()
            data["tracking_channel_id"] = channel.id
            save_tracking_data(data)
            
            channel_type = "forum" if isinstance(channel, discord.ForumChannel) else "text channel"
            
            embed = create_basic_embed(
                title="✅ Stalking Channel Set",
                description=f"Player stalking threads will be created in {channel.mention} ({channel_type})\n\n"
                           f"Use `/stalk add` to start stalking players!"
            )
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)
    
    @track_group.command(name="unset", description="Remove the stalking channel configuration")
    async def track_unset(interaction: discord.Interaction):
        """
        Unset/remove the stalking channel.
        
        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer()
        
        try:
            data = load_tracking_data()
            
            # Check if a channel is even set
            if not data.get("tracking_channel_id"):
                embed = create_error_embed(
                    "No stalking channel is currently set.\n\n"
                    "Use `/stalk set` to set one first."
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Check if there are tracked players
            tracked_count = len(data.get("tracked_players", []))
            
            if tracked_count > 0:
                embed = create_error_embed(
                    f"⚠️ Cannot unset stalking channel!\n\n"
                    f"You have **{tracked_count} player(s)** currently being stalked.\n\n"
                    f"Please remove all tracked players first using `/stalk remove`.\n"
                    f"Use `/stalk list` to see all tracked players."
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Get channel mention before removing
            channel_id = data["tracking_channel_id"]
            channel = interaction.guild.get_channel(channel_id)
            channel_mention = channel.mention if channel else f"Channel ID: {channel_id}"
            
            # Remove the stalking channel
            data["tracking_channel_id"] = None
            save_tracking_data(data)
            
            embed = create_basic_embed(
                title="✅ Stalking Channel Removed",
                description=f"The stalking channel ({channel_mention}) has been unset.\n\n"
                           f"Use `/stalk set` to set a new channel when needed."
            )
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)
    
    @track_group.command(name="add", description="Add a player to track (creates a thread)")
    @app_commands.describe(
        game_name="Player's game name (without tag)",
        tag_line="Player's tag (without #)"
    )
    async def track_add(
        interaction: discord.Interaction,
        game_name: str,
        tag_line: str
    ):
        """
        Add a player to track by creating a dedicated thread.
        
        Args:
            interaction: Discord interaction
            game_name: Player's game name
            tag_line: Player's tag
        """
        await interaction.response.defer()
        
        try:
            # Check if tracking channel is set
            data = load_tracking_data()
            
            if not data.get("tracking_channel_id"):
                embed = create_error_embed(
                    "No stalking channel set!\n\n"
                    "Use `/stalk set` to set a channel first."
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Get the tracking channel
            channel = interaction.guild.get_channel(data["tracking_channel_id"])
            
            if not channel:
                embed = create_error_embed(
                    "The stalking channel no longer exists!\n\n"
                    "Use `/stalk set` to set a new channel."
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Fetch summoner data to verify they exist (uses default region from config)
            summoner_data = await riot_api.get_summoner_by_riot_id(game_name, tag_line, config.DEFAULT_REGION)
            
            puuid = summoner_data["puuid"]
            verified_name = summoner_data["gameName"]
            verified_tag = summoner_data["tagLine"]
            full_name = f"{verified_name}#{verified_tag}"
            
            # Check if player is already tracked
            for player in data.get("tracked_players", []):
                if player["puuid"] == puuid:
                    embed = create_error_embed(
                        f"**{full_name}** is already being stalked!\n\n"
                        f"Thread: <#{player['thread_id']}>"
                    )
                    await interaction.followup.send(embed=embed)
                    return
            
            # Fetch rank data for the initial post
            rank_data = await riot_api.get_summoner_rank(puuid, config.DEFAULT_REGION)
            
            # Create embeds for initial post
            summoner_embed = create_summoner_embed(summoner_data)
            rank_embed = create_rank_embed(summoner_data, rank_data)
            
            initial_content = (
                f"**Now stalking {full_name}**\n"
                f"Region: {config.DEFAULT_REGION.upper()}\n"
                f"Added by: {interaction.user.mention}"
            )
            
            # Create thread differently based on channel type
            if isinstance(channel, discord.ForumChannel):
                # For forum channels, create a forum post (which is a thread)
                thread_with_message = await channel.create_thread(
                    name=f"👁️ {full_name}",
                    content=initial_content,
                    embeds=[summoner_embed, rank_embed],
                    reason=f"Stalking player {full_name}"
                )
                # For forum posts, we get a ThreadWithMessage object
                thread = thread_with_message.thread
                info_message = thread_with_message.message
            else:
                # For text channels, create a public thread
                thread = await channel.create_thread(
                    name=f"👁️ {full_name}",
                    type=discord.ChannelType.public_thread,
                    reason=f"Stalking player {full_name}"
                )
                
                # Send initial message in the thread
                info_message = await thread.send(
                    content=initial_content,
                    embeds=[summoner_embed, rank_embed]
                )
                
                # Pin the info message (only for text channel threads)
                await info_message.pin()
            
            # Add to tracked players
            if "tracked_players" not in data:
                data["tracked_players"] = []
            
            data["tracked_players"].append({
                "puuid": puuid,
                "game_name": verified_name,
                "tag_line": verified_tag,
                "region": config.DEFAULT_REGION.lower(),
                "thread_id": thread.id,
                "tracked_at": datetime.now().isoformat(),
                "tracked_by": interaction.user.id
            })
            
            save_tracking_data(data)
            
            # Send confirmation
            embed = create_basic_embed(
                title="✅ Player Stalked",
                description=f"**{full_name}** is now being stalked!\n\n"
                           f"Thread created: {thread.mention}\n"
                           f"Region: {config.DEFAULT_REGION.upper()}"
            )
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)
    
    @track_group.command(name="list", description="List all tracked players")
    async def track_list(interaction: discord.Interaction):
        """
        Show all currently tracked players.
        
        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer()
        
        try:
            data = load_tracking_data()
            
            if not data.get("tracked_players"):
                embed = create_basic_embed(
                    title="📋 Stalked Players",
                    description="No players are currently being stalked.\n\nUse `/stalk add` to start stalking!"
                )
                await interaction.followup.send(embed=embed)
                return
            
            tracking_channel_id = data.get("tracking_channel_id")
            channel_mention = f"<#{tracking_channel_id}>" if tracking_channel_id else "None set"
            
            embed = create_basic_embed(
                title="📋 Stalked Players",
                description=f"**Stalking Channel:** {channel_mention}\n\n"
                           f"**{len(data['tracked_players'])} player(s) stalked:**"
            )
            
            for i, player in enumerate(data["tracked_players"], 1):
                full_name = f"{player['game_name']}#{player['tag_line']}"
                region = player['region'].upper()
                thread_id = player['thread_id']
                tracked_at = datetime.fromisoformat(player['tracked_at']).strftime("%Y-%m-%d")
                
                embed.add_field(
                    name=f"{i}. {full_name}",
                    value=f"Region: {region} | Thread: <#{thread_id}>\nTracked: {tracked_at}",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)
    
    @track_group.command(name="remove", description="Stop tracking a player (archives the thread)")
    @app_commands.describe(
        game_name="Player's game name (without tag)",
        tag_line="Player's tag (without #)"
    )
    async def track_remove(
        interaction: discord.Interaction,
        game_name: str,
        tag_line: str
    ):
        """
        Remove a player from tracking and archive their thread.
        
        Args:
            interaction: Discord interaction
            game_name: Player's game name
            tag_line: Player's tag
        """
        await interaction.response.defer()
        
        try:
            data = load_tracking_data()
            
            # Find the player
            player_to_remove = None
            for player in data.get("tracked_players", []):
                if (player["game_name"].lower() == game_name.lower() and 
                    player["tag_line"].lower() == tag_line.lower()):
                    player_to_remove = player
                    break
            
            if not player_to_remove:
                embed = create_error_embed(
                    f"**{game_name}#{tag_line}** is not being stalked."
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Archive the thread
            try:
                thread = interaction.guild.get_thread(player_to_remove["thread_id"])
                if thread:
                    await thread.edit(archived=True, locked=True)
            except:
                pass  # Thread might already be deleted
            
            # Remove from tracked list
            data["tracked_players"].remove(player_to_remove)
            save_tracking_data(data)
            
            full_name = f"{player_to_remove['game_name']}#{player_to_remove['tag_line']}"
            
            embed = create_basic_embed(
                title="✅ Player Removed",
                description=f"**{full_name}** is no longer being stalked.\n\nTheir thread has been archived."
            )
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)
    
    # Add the command group to the bot
    bot.tree.add_command(track_group)


# ==================== MONITORING SYSTEM ====================

async def monitor_players(bot: commands.Bot):
    """
    Background monitoring function that checks stalked players.
    Detects: Live games, new matches, duo partners.
    """
    data = load_tracking_data()
    
    if not data.get("tracking_channel_id") or not data.get("tracked_players"):
        return  # Nothing to monitor
    
    print(f"[Monitor] Checking {len(data['tracked_players'])} stalked players...")
    
    for player in data["tracked_players"]:
        try:
            await check_player_activity(bot, player, data)
        except Exception as e:
            print(f"[Monitor] Error checking {player['game_name']}#{player['tag_line']}: {e}")
    
    # Save any updates
    save_tracking_data(data)


async def check_player_activity(bot: commands.Bot, player: dict, data: dict):
    """Check a single player for activity and post updates."""
    puuid = player["puuid"]
    region = player["region"]
    thread_id = player["thread_id"]
    full_name = f"{player['game_name']}#{player['tag_line']}"
    
    # Get the thread
    thread = bot.get_channel(thread_id)
    if not thread:
        # Try fetching the thread
        try:
            thread = await bot.fetch_channel(thread_id)
        except:
            print(f"[Monitor] Thread not found for {full_name}")
            return
    
    # Initialize tracking data if not exists
    if "last_match_id" not in player:
        player["last_match_id"] = None
    if "is_in_game" not in player:
        player["is_in_game"] = False
    if "duo_partners" not in player:
        player["duo_partners"] = {}  # {puuid: {name, count}}
    
    # Check if player is in a live game
    await check_live_game(thread, player, puuid, region, full_name)
    
    # Check for new matches
    await check_new_matches(thread, player, puuid, region, full_name)


async def check_live_game(thread, player: dict, puuid: str, region: str, full_name: str):
    """Check if player is currently in a game."""
    try:
        active_game = await riot_api.get_active_game(puuid, region)
        
        if active_game and not player["is_in_game"]:
            # Player just started a game!
            player["is_in_game"] = True
            
            # Get champion data
            champion_data = await riot_api.get_champion_data()
            
            # Find player's champion
            player_champ = "Unknown"
            for participant in active_game.get("participants", []):
                if participant.get("puuid") == puuid:
                    champ_id = participant.get("championId")
                    player_champ = riot_api.get_champion_name_by_id(champ_id, champion_data)
                    break
            
            # Get game mode using queue ID (same as match results for consistency)
            queue_id = active_game.get("gameQueueConfigId", 0)
            game_mode = get_game_mode_name(queue_id)
            
            # Post to thread
            embed = discord.Embed(
                title="🎮 Live Game Started!",
                description=f"**{full_name}** is now in game!",
                color=0x00FF00,
                timestamp=datetime.now()
            )
            embed.add_field(name="Playing As", value=player_champ, inline=True)
            embed.add_field(name="Game Mode", value=game_mode, inline=True)
            
            await thread.send(embed=embed)
            print(f"[Monitor] {full_name} started a game as {player_champ} ({game_mode})")
        
        elif not active_game and player["is_in_game"]:
            # Player finished their game
            player["is_in_game"] = False
            print(f"[Monitor] {full_name} finished their game")
    
    except Exception as e:
        print(f"[Monitor] Error checking live game for {full_name}: {e}")


async def check_new_matches(thread, player: dict, puuid: str, region: str, full_name: str):
    """Check for new matches and post results."""
    try:
        # Get recent match history
        match_ids = await riot_api.get_match_history(puuid, region, count=1)
        
        if not match_ids:
            return
        
        latest_match_id = match_ids[0]
        
        # Check if this is a new match
        if player["last_match_id"] == latest_match_id:
            return  # No new matches
        
        # New match detected!
        player["last_match_id"] = latest_match_id
        
        # Get match details
        match_details = await riot_api.get_match_details(latest_match_id, region)
        champion_data = await riot_api.get_champion_data()
        
        # Find player's data in the match
        participant = None
        for p in match_details["info"]["participants"]:
            if p["puuid"] == puuid:
                participant = p
                break
        
        if not participant:
            return
        
        # Extract match data
        champion_name = riot_api.get_champion_name_by_id(participant["championId"], champion_data)
        kills = participant["kills"]
        deaths = participant["deaths"]
        assists = participant["assists"]
        win = participant["win"]
        
        kda = f"{kills}/{deaths}/{assists}"
        kda_ratio = round((kills + assists) / deaths, 2) if deaths > 0 else float(kills + assists)
        
        duration_seconds = match_details["info"]["gameDuration"]
        duration_minutes = duration_seconds // 60
        
        # Get game mode
        queue_id = match_details["info"].get("queueId", 0)
        game_mode = get_game_mode_name(queue_id)
        
        # Check if this is a ranked solo/duo game
        is_ranked_solo = (queue_id == 420)
        
        # Check for duo partners
        duo_info = await detect_duo_partners(match_details, player, puuid, champion_data)
        
        # Fetch current rank data for LP tracking (ONLY for ranked solo/duo)
        rank_change_info = None
        if is_ranked_solo:
            rank_change_info = await check_rank_change(player, puuid, region)
        
        # Create result embed
        color = 0x00FF00 if win else 0xFF0000
        result_text = "✅ Victory" if win else "❌ Defeat"
        
        embed = discord.Embed(
            title=f"{result_text} - New Match Detected!",
            description=f"**{full_name}** just finished a match!",
            color=color,
            timestamp=datetime.now()
        )
        embed.add_field(name="Champion", value=champion_name, inline=True)
        embed.add_field(name="KDA", value=f"{kda} ({kda_ratio})", inline=True)
        embed.add_field(name="Game Mode", value=game_mode, inline=True)
        embed.add_field(name="Duration", value=f"{duration_minutes}min", inline=True)
        
        # Add rank change if available (only for ranked games)
        if rank_change_info:
            embed.add_field(name="📊 Rank Change", value=rank_change_info, inline=False)
        
        if duo_info:
            embed.add_field(name="🤝 Duo Partners", value=duo_info, inline=False)
        
        await thread.send(embed=embed)
        
        # Check for promotion/demotion (only for ranked games)
        if is_ranked_solo:
            promo_message = await check_promotion_demotion(player, thread, full_name)
            if promo_message:
                await thread.send(promo_message)
        
        print(f"[Monitor] {full_name} finished match: {result_text} as {champion_name} ({game_mode})")
    
    except Exception as e:
        print(f"[Monitor] Error checking matches for {full_name}: {e}")


async def detect_duo_partners(match_details: dict, player: dict, player_puuid: str, champion_data: dict):
    """
    Detect if player is playing with the same teammates repeatedly.
    Returns a string with duo partner info, or None.
    """
    try:
        # Get player's team
        player_team = None
        for p in match_details["info"]["participants"]:
            if p["puuid"] == player_puuid:
                player_team = p["teamId"]
                break
        
        if not player_team:
            return None
        
        duo_partners = player.get("duo_partners", {})
        duo_messages = []
        
        # Check all teammates
        for p in match_details["info"]["participants"]:
            if p["puuid"] == player_puuid or p["teamId"] != player_team:
                continue  # Skip self and enemies
            
            teammate_puuid = p["puuid"]
            teammate_name = p.get("riotIdGameName", "Unknown") + "#" + p.get("riotIdTagLine", "????")
            teammate_champ = riot_api.get_champion_name_by_id(p["championId"], champion_data)
            
            # Track this duo partner
            if teammate_puuid not in duo_partners:
                duo_partners[teammate_puuid] = {
                    "name": teammate_name,
                    "count": 1
                }
            else:
                duo_partners[teammate_puuid]["count"] += 1
                count = duo_partners[teammate_puuid]["count"]
                
                # If they've played together 3+ times, mention it
                if count >= 3:
                    duo_messages.append(f"**{teammate_name}** ({teammate_champ}) - {count} games together")
        
        # Update duo_partners in player data
        player["duo_partners"] = duo_partners
        
        if duo_messages:
            return "\n".join(duo_messages)
        
        return None
    
    except Exception as e:
        print(f"[Monitor] Error detecting duo partners: {e}")
        return None


async def check_rank_change(player: dict, puuid: str, region: str) -> str:
    """
    Check for LP/rank changes and return a formatted string.
    Returns None if no ranked data or no change to display.
    """
    try:
        # Fetch current rank data
        rank_data = await riot_api.get_summoner_rank(puuid, region)
        
        # Find Solo/Duo queue
        current_solo = None
        for queue in rank_data:
            if queue.get("queueType") == "RANKED_SOLO_5x5":
                current_solo = queue
                break
        
        if not current_solo:
            return None  # Not ranked
        
        # Extract current rank info
        current_tier = current_solo.get("tier", "")
        current_rank = current_solo.get("rank", "")
        current_lp = current_solo.get("leaguePoints", 0)
        
        # Initialize previous rank if not exists
        if "last_rank" not in player:
            player["last_rank"] = {
                "tier": current_tier,
                "rank": current_rank,
                "lp": current_lp
            }
            return None  # First time tracking, no change to show
        
        # Get previous rank
        prev_tier = player["last_rank"].get("tier", "")
        prev_rank = player["last_rank"].get("rank", "")
        prev_lp = player["last_rank"].get("lp", 0)
        
        # Calculate LP change
        lp_change = current_lp - prev_lp
        
        # Update stored rank
        player["last_rank"] = {
            "tier": current_tier,
            "rank": current_rank,
            "lp": current_lp
        }
        
        # Format rank display
        rank_display = f"{current_tier.capitalize()} {current_rank} {current_lp} LP"
        
        # If LP changed, show the change
        if lp_change != 0:
            change_emoji = "📈" if lp_change > 0 else "📉"
            sign = "+" if lp_change > 0 else ""
            return f"{rank_display} ({sign}{lp_change} LP) {change_emoji}"
        
        # No change
        return f"{rank_display}"
    
    except Exception as e:
        print(f"[Monitor] Error checking rank change: {e}")
        return None


async def check_promotion_demotion(player: dict, thread, full_name: str) -> str:
    """
    Check if player was promoted or demoted and return a special message.
    Returns None if no promotion/demotion occurred.
    """
    try:
        if "last_rank" not in player or "prev_last_rank" not in player:
            # Store current as previous for next check
            if "last_rank" in player:
                player["prev_last_rank"] = player["last_rank"].copy()
            return None
        
        current = player["last_rank"]
        previous = player.get("prev_last_rank", {})
        
        current_tier = current.get("tier", "")
        current_rank = current.get("rank", "")
        prev_tier = previous.get("tier", "")
        prev_rank = previous.get("rank", "")
        
        # Update prev_last_rank for next check
        player["prev_last_rank"] = current.copy()
        
        # Check for promotion/demotion
        tier_order = {"IRON": 1, "BRONZE": 2, "SILVER": 3, "GOLD": 4, "PLATINUM": 5, 
                      "EMERALD": 6, "DIAMOND": 7, "MASTER": 8, "GRANDMASTER": 9, "CHALLENGER": 10}
        rank_order = {"IV": 1, "III": 2, "II": 3, "I": 4}
        
        current_tier_val = tier_order.get(current_tier, 0)
        prev_tier_val = tier_order.get(prev_tier, 0)
        current_rank_val = rank_order.get(current_rank, 0)
        prev_rank_val = rank_order.get(prev_rank, 0)
        
        # Promotion
        if (current_tier_val > prev_tier_val) or \
           (current_tier_val == prev_tier_val and current_rank_val > prev_rank_val):
            return f"🎉 **PROMOTION!** {full_name} has been promoted to **{current_tier.capitalize()} {current_rank}**! 🎉"
        
        # Demotion
        elif (current_tier_val < prev_tier_val) or \
             (current_tier_val == prev_tier_val and current_rank_val < prev_rank_val):
            return f"😢 {full_name} was demoted to **{current_tier.capitalize()} {current_rank}**"
        
        return None
    
    except Exception as e:
        print(f"[Monitor] Error checking promotion/demotion: {e}")
        return None


def get_game_mode_name(queue_id: int) -> str:
    """
    Convert queue ID to readable game mode name.
    
    Args:
        queue_id: Riot API queue ID
        
    Returns:
        Human-readable game mode name
    """
    queue_names = {
        0: "Custom Game",
        400: "Normal Draft",
        420: "Ranked Solo/Duo",
        430: "Normal Blind",
        440: "Ranked Flex",
        450: "ARAM",
        700: "Clash",
        830: "Co-op vs AI (Intro)",
        840: "Co-op vs AI (Beginner)",
        850: "Co-op vs AI (Intermediate)",
        900: "URF",
        1020: "One For All",
        1300: "Nexus Blitz",
        1400: "Ultimate Spellbook",
        1700: "Arena",
        1900: "Pick URF",
        2000: "Tutorial"
    }
    
    return queue_names.get(queue_id, f"Unknown Mode ({queue_id})")
