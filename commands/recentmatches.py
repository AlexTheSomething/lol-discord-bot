"""
Recent Matches command - Display recent match history.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import (
    create_basic_embed, create_error_embed, get_region_choices,
    format_kda, calculate_kda_ratio, format_duration, format_timestamp
)
import config


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="recentmatches", description="Display last 5 matches")
    @app_commands.describe(
        game_name="Summoner's game name (without tag)",
        tag_line="Summoner's tag (without #)",
        region="Region (default: EUN1)"
    )
    @app_commands.choices(region=get_region_choices())
    async def recentmatches(
        interaction: discord.Interaction,
        game_name: str,
        tag_line: str,
        region: str = config.DEFAULT_REGION
    ):
        """
        Display last 5 matches with KDA, champion, and result.
        
        Args:
            interaction: Discord interaction
            game_name: Summoner's game name
            tag_line: Summoner's tag
            region: Region code
        """
        await interaction.response.defer()
        
        try:
            # Fetch summoner data
            summoner_data = await riot_api.get_summoner_by_riot_id(game_name, tag_line, region)
            puuid = summoner_data["puuid"]
            
            # Fetch match history
            match_ids = await riot_api.get_match_history(puuid, region, count=5)
            
            if not match_ids:
                embed = create_basic_embed(
                    title=f"Recent Matches - {game_name}#{tag_line}",
                    description="No recent matches found"
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Fetch champion data for name lookup
            champion_data = await riot_api.get_champion_data()
            
            embed = create_basic_embed(
                title=f"Recent Matches - {game_name}#{tag_line}",
                description=f"Last {len(match_ids)} matches"
            )
            
            # Process each match
            for i, match_id in enumerate(match_ids, 1):
                try:
                    match_details = await riot_api.get_match_details(match_id, region)
                    
                    # Find player's data in the match
                    participant = None
                    for p in match_details["info"]["participants"]:
                        if p["puuid"] == puuid:
                            participant = p
                            break
                    
                    if participant:
                        # Extract match data
                        champion_name = riot_api.get_champion_name_by_id(
                            participant["championId"], champion_data
                        )
                        kills = participant["kills"]
                        deaths = participant["deaths"]
                        assists = participant["assists"]
                        win = participant["win"]
                        
                        kda_str = format_kda(kills, deaths, assists)
                        kda_ratio = calculate_kda_ratio(kills, deaths, assists)
                        duration = format_duration(match_details["info"]["gameDuration"])
                        
                        result = "✅ Victory" if win else "❌ Defeat"
                        
                        embed.add_field(
                            name=f"Match {i} - {result}",
                            value=f"**{champion_name}** | {kda_str} (KDA: {kda_ratio})\nDuration: {duration}",
                            inline=False
                        )
                
                except Exception as e:
                    embed.add_field(
                        name=f"Match {i}",
                        value=f"Error loading match data",
                        inline=False
                    )
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

