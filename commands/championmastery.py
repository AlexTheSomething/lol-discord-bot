"""
Champion Mastery command - Display top champions by mastery points.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_basic_embed, create_error_embed
import config


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="championmastery", description="Display top 5 champions by mastery")
    @app_commands.describe(
        game_name="Summoner's game name (without tag)",
        tag_line="Summoner's tag (without #)"
    )
    async def championmastery(
        interaction: discord.Interaction,
        game_name: str,
        tag_line: str
    ):
        """
        Display top 5 champions by mastery points.
        
        Args:
            interaction: Discord interaction
            game_name: Summoner's game name
            tag_line: Summoner's tag
        """
        await interaction.response.defer()
        
        try:
            # Fetch summoner data (uses default region from config)
            summoner_data = await riot_api.get_summoner_by_riot_id(game_name, tag_line, config.DEFAULT_REGION)
            puuid = summoner_data["puuid"]
            
            # Fetch champion mastery data
            mastery_data = await riot_api.get_champion_mastery(puuid, config.DEFAULT_REGION, count=5)
            
            if not mastery_data:
                embed = create_basic_embed(
                    title=f"Champion Mastery - {game_name}#{tag_line}",
                    description="No champion mastery data found"
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Fetch champion data for name lookup
            champion_data = await riot_api.get_champion_data()
            
            embed = create_basic_embed(
                title=f"Top Champions - {game_name}#{tag_line}",
                description="Top 5 champions by mastery points"
            )
            
            # Add each champion
            for i, mastery in enumerate(mastery_data, 1):
                champion_id = mastery["championId"]
                champion_name = riot_api.get_champion_name_by_id(champion_id, champion_data)
                
                mastery_level = mastery.get("championLevel", 0)
                mastery_points = mastery.get("championPoints", 0)
                
                # Format mastery points with comma separator
                points_formatted = f"{mastery_points:,}"
                
                # Mastery level emojis
                level_display = f"Level {mastery_level}"
                if mastery_level >= 7:
                    level_display = f"🏆 {level_display}"
                elif mastery_level >= 5:
                    level_display = f"⭐ {level_display}"
                
                embed.add_field(
                    name=f"{i}. {champion_name}",
                    value=f"{level_display}\n{points_formatted} points",
                    inline=True
                )
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

