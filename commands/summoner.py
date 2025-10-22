"""
Summoner command - Display summoner information.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_summoner_embed, create_error_embed, get_region_choices
import config


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="summoner", description="Display summoner information")
    @app_commands.describe(
        game_name="Summoner's game name (without tag)",
        tag_line="Summoner's tag (without #)",
        region="Region (default: EUN1)"
    )
    @app_commands.choices(region=get_region_choices())
    async def summoner(
        interaction: discord.Interaction,
        game_name: str,
        tag_line: str,
        region: str = config.DEFAULT_REGION
    ):
        """
        Display summoner level, profile icon, and region.
        
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
            
            # Create and send embed
            embed = create_summoner_embed(summoner_data)
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

