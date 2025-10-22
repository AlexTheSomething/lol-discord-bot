"""
Rank command - Display ranked information.
TEMPORARILY DISABLED: Riot API not returning summoner ID field needed for ranked data.
"""

# import discord
# from discord import app_commands
# from discord.ext import commands
# import riot_api
# from utils.helpers import create_rank_embed, create_error_embed, get_region_choices
# import config


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    pass  # Command disabled due to Riot API limitations
    
    # @bot.tree.command(name="rank", description="Display ranked stats and winrate")
    # @app_commands.describe(
    #     game_name="Summoner's game name (without tag)",
    #     tag_line="Summoner's tag (without #)",
    #     region="Region (default: EUN1)"
    # )
    # @app_commands.choices(region=get_region_choices())
    # async def rank(
    #     interaction: discord.Interaction,
    #     game_name: str,
    #     tag_line: str,
    #     region: str = config.DEFAULT_REGION
    # ):
    #     """
    #     Display summoner's rank, LP, and winrate.
    #     
    #     Args:
    #         interaction: Discord interaction
    #         game_name: Summoner's game name
    #         tag_line: Summoner's tag
    #         region: Region code
    #     """
    #     await interaction.response.defer()
    #     
    #     try:
    #         # Fetch summoner data
    #         summoner_data = await riot_api.get_summoner_by_riot_id(game_name, tag_line, region)
    #         
    #         # Fetch rank data
    #         rank_data = await riot_api.get_summoner_rank(summoner_data["puuid"], region)
    #         
    #         # Create and send embed
    #         embed = create_rank_embed(summoner_data, rank_data)
    #         await interaction.followup.send(embed=embed)
    #     
    #     except riot_api.RiotAPIError as e:
    #         embed = create_error_embed(str(e))
    #         await interaction.followup.send(embed=embed)
    #     
    #     except Exception as e:
    #         embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
    #         await interaction.followup.send(embed=embed)

