"""
Rotation command - Display current free champion rotation.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_basic_embed, create_error_embed, get_region_choices
import config


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="rotation", description="Display current free champion rotation")
    @app_commands.describe(region="Region (default: EUN1)")
    @app_commands.choices(region=get_region_choices())
    async def rotation(
        interaction: discord.Interaction,
        region: str = config.DEFAULT_REGION
    ):
        """
        Display current free champion rotation.
        
        Args:
            interaction: Discord interaction
            region: Region code
        """
        await interaction.response.defer()
        
        try:
            # Fetch rotation data
            rotation_data = await riot_api.get_champion_rotation(region)
            
            free_champion_ids = rotation_data.get("freeChampionIds", [])
            
            if not free_champion_ids:
                embed = create_basic_embed(
                    title="Free Champion Rotation",
                    description="No free champions available"
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Fetch champion data for name lookup
            champion_data = await riot_api.get_champion_data()
            
            # Get champion names
            champion_names = []
            for champ_id in free_champion_ids:
                name = riot_api.get_champion_name_by_id(champ_id, champion_data)
                champion_names.append(name)
            
            # Sort alphabetically
            champion_names.sort()
            
            # Format into columns
            champions_text = ", ".join(champion_names)
            
            embed = create_basic_embed(
                title="🎮 Free Champion Rotation",
                description=f"**{len(champion_names)} champions available this week**\n\n{champions_text}"
            )
            
            embed.add_field(
                name="Region",
                value=region.upper(),
                inline=False
            )
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

