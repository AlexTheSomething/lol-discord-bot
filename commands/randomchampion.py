"""
Random Champion command - Suggest a random champion.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_basic_embed, create_error_embed, get_champion_icon_url
import random


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="randomchampion", description="Get a random champion suggestion")
    @app_commands.describe(
        from_rotation="Only choose from free rotation champions"
    )
    async def randomchampion(
        interaction: discord.Interaction,
        from_rotation: bool = False
    ):
        """
        Suggest a random champion from all champions or free rotation.
        
        Args:
            interaction: Discord interaction
            from_rotation: If True, only select from free rotation
        """
        await interaction.response.defer()
        
        try:
            # Fetch champion data
            champion_data = await riot_api.get_champion_data()
            
            if from_rotation:
                # Get free rotation
                rotation_data = await riot_api.get_champion_rotation()
                free_champion_ids = rotation_data.get("freeChampionIds", [])
                
                if not free_champion_ids:
                    embed = create_error_embed("No free champions available")
                    await interaction.followup.send(embed=embed)
                    return
                
                # Pick random from rotation
                random_id = random.choice(free_champion_ids)
                champion_name = riot_api.get_champion_name_by_id(random_id, champion_data)
                source = "Free Rotation"
            else:
                # Pick random from all champions
                all_champions = list(champion_data.get("data", {}).values())
                
                if not all_champions:
                    embed = create_error_embed("Could not load champion data")
                    await interaction.followup.send(embed=embed)
                    return
                
                random_champion = random.choice(all_champions)
                champion_name = random_champion.get("name", "Unknown")
                source = "All Champions"
            
            # Get champion icon URL
            # We need to find the champion key (internal name) for the icon
            champion_key = None
            for champ_key, champ_info in champion_data.get("data", {}).items():
                if champ_info.get("name") == champion_name:
                    champion_key = champ_key
                    break
            
            embed = create_basic_embed(
                title="🎲 Random Champion",
                description=f"**{champion_name}**"
            )
            
            embed.add_field(name="Source", value=source, inline=False)
            
            if champion_key:
                embed.set_thumbnail(url=get_champion_icon_url(champion_key))
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

