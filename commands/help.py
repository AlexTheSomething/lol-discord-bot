"""
Help command - Display list of available commands.
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import create_basic_embed
import config


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="help", description="Show all available commands")
    async def help_command(interaction: discord.Interaction):
        """
        Display all available bot commands with descriptions.
        
        Args:
            interaction: Discord interaction
        """
        embed = create_basic_embed(
            title="📚 League of Legends Bot - Help",
            description="Here are all available commands:"
        )
        
        # Data Display Commands
        embed.add_field(
            name="📊 Data Display Commands",
            value=(
                "`/summoner` - Display summoner information\n"
                "`/recentmatches` - Display last 5 matches\n"
                "`/championmastery` - Show top 5 champions\n"
                "`/rotation` - Current free champion rotation\n"
                "~~`/rank`~~ - Temporarily disabled\n"
                "~~`/livegame`~~ - Temporarily disabled"
            ),
            inline=False
        )
        
        # Tracking Commands
        embed.add_field(
            name="👁️ Player Stalking (Thread-Based)",
            value=(
                "`/stalk set` - Set stalking channel\n"
                "`/stalk add` - Stalk a player (creates thread)\n"
                "`/stalk list` - List all stalked players\n"
                "`/stalk remove` - Stop stalking a player\n"
                "`/compare` - Compare two summoners"
            ),
            inline=False
        )
        
        # Utility Commands
        embed.add_field(
            name="🛠️ Utility Commands",
            value=(
                "`/randomchampion` - Get random champion suggestion\n"
                "`/build` - Get build resources for a champion\n"
                "`/ping` - Check bot latency\n"
                "`/help` - Show this help message\n"
                "`/about` - Bot information"
            ),
            inline=False
        )
        
        # Usage Tips
        embed.add_field(
            name="💡 Usage Tips",
            value=(
                "• Use Riot ID format: `GameName#TAG`\n"
                f"• Default region is **{config.DEFAULT_REGION.upper()}**\n"
                "• Most commands support region selection\n"
                "• Track summoners to build a leaderboard!"
            ),
            inline=False
        )
        
        embed.set_footer(text="Powered by Riot Games API")
        
        await interaction.response.send_message(embed=embed)

