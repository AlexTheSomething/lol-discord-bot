"""
Live Game command - Display current match if player is in game.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_basic_embed, create_error_embed, format_duration
import config


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="livegame", description="Display current match if player is in game")
    @app_commands.describe(
        game_name="Summoner's game name (without tag)",
        tag_line="Summoner's tag (without #)"
    )
    async def livegame(
        interaction: discord.Interaction,
        game_name: str,
        tag_line: str
    ):
        """
        Display current match details if player is in game.
        
        Args:
            interaction: Discord interaction
            game_name: Summoner's game name
            tag_line: Summoner's tag
        """
        await interaction.response.defer()
        
        try:
            # Fetch summoner data
            summoner_data = await riot_api.get_summoner_by_riot_id(game_name, tag_line, config.DEFAULT_REGION)
            puuid = summoner_data["puuid"]
            
            # Fetch active game data
            active_game = await riot_api.get_active_game(puuid, config.DEFAULT_REGION)
            
            if not active_game:
                embed = create_basic_embed(
                    title=f"Live Game - {game_name}#{tag_line}",
                    description="❌ This player is not currently in a game"
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Fetch champion data for name lookup
            champion_data = await riot_api.get_champion_data()
            
            # Extract game mode
            game_mode = active_game.get("gameMode", "Unknown")
            game_type = active_game.get("gameType", "Unknown")
            game_length = active_game.get("gameLength", 0)
            
            embed = create_basic_embed(
                title=f"🎮 Live Game - {game_name}#{tag_line}",
                description=f"**Mode:** {game_mode}\n**Type:** {game_type}\n**Duration:** {format_duration(game_length)}"
            )
            
            # Find the player's champion
            player_participant = None
            for participant in active_game.get("participants", []):
                if participant.get("puuid") == puuid:
                    player_participant = participant
                    break
            
            if player_participant:
                champion_id = player_participant.get("championId")
                champion_name = riot_api.get_champion_name_by_id(champion_id, champion_data)
                
                embed.add_field(
                    name="Playing As",
                    value=f"**{champion_name}**",
                    inline=True
                )
            
            # Count teams
            team_100 = []
            team_200 = []
            
            for participant in active_game.get("participants", []):
                champ_id = participant.get("championId")
                champ_name = riot_api.get_champion_name_by_id(champ_id, champion_data)
                
                if participant.get("teamId") == 100:
                    team_100.append(champ_name)
                else:
                    team_200.append(champ_name)
            
            if team_100:
                embed.add_field(
                    name="🔵 Blue Team",
                    value="\n".join(team_100),
                    inline=True
                )
            
            if team_200:
                embed.add_field(
                    name="🔴 Red Team",
                    value="\n".join(team_200),
                    inline=True
                )
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

