"""
Build command - Provide links to champion build resources.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_basic_embed, create_error_embed


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="build", description="Get build resources for a champion")
    @app_commands.describe(
        champion_name="Champion name (e.g., 'Ahri', 'Lee Sin')"
    )
    async def build(
        interaction: discord.Interaction,
        champion_name: str
    ):
        """
        Provide links to champion build resources.
        
        Args:
            interaction: Discord interaction
            champion_name: Name of the champion
        """
        await interaction.response.defer()
        
        try:
            # Fetch champion data to verify the champion exists
            champion_data = await riot_api.get_champion_data()
            
            # Find the champion (case-insensitive search)
            found_champion = None
            champion_key = None
            
            for champ_key, champ_info in champion_data.get("data", {}).items():
                if champ_info.get("name", "").lower() == champion_name.lower():
                    found_champion = champ_info.get("name")
                    champion_key = champ_key
                    break
            
            if not found_champion:
                embed = create_error_embed(
                    f"Champion '{champion_name}' not found. Please check the spelling and try again."
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Format champion name for URLs (replace spaces with hyphens, lowercase)
            url_name = found_champion.replace(" ", "-").replace("'", "").lower()
            champion_id = champion_key.lower()
            
            # Create build resource links
            opgg_link = f"https://www.op.gg/champions/{url_name}/build"
            ugg_link = f"https://u.gg/lol/champions/{champion_id}/build"
            mobafire_link = f"https://www.mobafire.com/league-of-legends/{url_name}-guide"
            
            embed = create_basic_embed(
                title=f"📖 {found_champion} Build Resources",
                description=f"Here are some popular build guides for **{found_champion}**:"
            )
            
            embed.add_field(
                name="🔷 OP.GG",
                value=f"[View Build on OP.GG]({opgg_link})",
                inline=False
            )
            
            embed.add_field(
                name="🔶 U.GG",
                value=f"[View Build on U.GG]({ugg_link})",
                inline=False
            )
            
            embed.add_field(
                name="📚 Mobafire",
                value=f"[View Guides on Mobafire]({mobafire_link})",
                inline=False
            )
            
            embed.set_footer(text="These sites provide pro builds, runes, items, and skill orders")
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

