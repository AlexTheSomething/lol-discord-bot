"""
Compare command - Compare two summoners side by side.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_basic_embed, create_error_embed, format_rank, calculate_winrate, get_region_choices
import config


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="compare", description="Compare two summoners side by side")
    @app_commands.describe(
        game_name1="First summoner's game name",
        tag_line1="First summoner's tag",
        game_name2="Second summoner's game name",
        tag_line2="Second summoner's tag",
        region="Region (default: EUN1)"
    )
    @app_commands.choices(region=get_region_choices())
    async def compare(
        interaction: discord.Interaction,
        game_name1: str,
        tag_line1: str,
        game_name2: str,
        tag_line2: str,
        region: str = config.DEFAULT_REGION
    ):
        """
        Compare two summoners side by side.
        
        Args:
            interaction: Discord interaction
            game_name1: First summoner's game name
            tag_line1: First summoner's tag
            game_name2: Second summoner's game name
            tag_line2: Second summoner's tag
            region: Region code
        """
        await interaction.response.defer()
        
        try:
            # Fetch both summoners
            summoner1 = await riot_api.get_summoner_by_riot_id(game_name1, tag_line1, region)
            summoner2 = await riot_api.get_summoner_by_riot_id(game_name2, tag_line2, region)
            
            # Fetch rank data
            rank1 = await riot_api.get_summoner_rank(summoner1["puuid"], region)
            rank2 = await riot_api.get_summoner_rank(summoner2["puuid"], region)
            
            # Fetch champion mastery
            mastery1 = await riot_api.get_champion_mastery(summoner1["puuid"], region, count=1)
            mastery2 = await riot_api.get_champion_mastery(summoner2["puuid"], region, count=1)
            
            # Get champion data
            champion_data = await riot_api.get_champion_data()
            
            # Extract Solo/Duo rank
            solo1 = None
            solo2 = None
            
            for queue in rank1:
                if queue.get("queueType") == "RANKED_SOLO_5x5":
                    solo1 = queue
                    break
            
            for queue in rank2:
                if queue.get("queueType") == "RANKED_SOLO_5x5":
                    solo2 = queue
                    break
            
            # Format data for summoner 1
            name1 = f"{summoner1['gameName']}#{summoner1['tagLine']}"
            level1 = summoner1.get("summonerLevel", "N/A")
            rank_str1 = format_rank(solo1) if solo1 else "Unranked"
            wins1 = solo1.get("wins", 0) if solo1 else 0
            losses1 = solo1.get("losses", 0) if solo1 else 0
            winrate1 = calculate_winrate(wins1, losses1)
            
            top_champ1 = "None"
            if mastery1:
                champ_id1 = mastery1[0]["championId"]
                top_champ1 = riot_api.get_champion_name_by_id(champ_id1, champion_data)
                top_champ1 += f" (M{mastery1[0].get('championLevel', 0)})"
            
            # Format data for summoner 2
            name2 = f"{summoner2['gameName']}#{summoner2['tagLine']}"
            level2 = summoner2.get("summonerLevel", "N/A")
            rank_str2 = format_rank(solo2) if solo2 else "Unranked"
            wins2 = solo2.get("wins", 0) if solo2 else 0
            losses2 = solo2.get("losses", 0) if solo2 else 0
            winrate2 = calculate_winrate(wins2, losses2)
            
            top_champ2 = "None"
            if mastery2:
                champ_id2 = mastery2[0]["championId"]
                top_champ2 = riot_api.get_champion_name_by_id(champ_id2, champion_data)
                top_champ2 += f" (M{mastery2[0].get('championLevel', 0)})"
            
            # Create comparison embed
            embed = create_basic_embed(
                title="⚔️ Summoner Comparison",
                description=f"**{name1}** vs **{name2}**\nRegion: {region.upper()}"
            )
            
            # Level comparison
            embed.add_field(
                name="📊 Level",
                value=f"{level1} vs {level2}",
                inline=False
            )
            
            # Rank comparison
            embed.add_field(
                name="🏆 Ranked Solo/Duo",
                value=f"{rank_str1}\nvs\n{rank_str2}",
                inline=False
            )
            
            # Winrate comparison
            embed.add_field(
                name="📈 Win Rate",
                value=f"{wins1}W {losses1}L ({winrate1}%)\nvs\n{wins2}W {losses2}L ({winrate2}%)",
                inline=False
            )
            
            # Top mastery comparison
            embed.add_field(
                name="⭐ Top Champion",
                value=f"{top_champ1}\nvs\n{top_champ2}",
                inline=False
            )
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

