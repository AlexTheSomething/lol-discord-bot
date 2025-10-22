"""
About command - Display bot information.
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import create_basic_embed


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="about", description="Learn more about this bot")
    async def about(interaction: discord.Interaction):
        """
        Display bot information and credits.
        
        Args:
            interaction: Discord interaction
        """
        embed = create_basic_embed(
            title="ℹ️ About League of Legends Bot",
            description=(
                "A Discord bot that integrates with the Riot Games API to "
                "provide League of Legends player statistics and information."
            )
        )
        
        embed.add_field(
            name="🔧 Version",
            value="1.0.0",
            inline=True
        )
        
        embed.add_field(
            name="💻 Language",
            value="Python 3.10+",
            inline=True
        )
        
        embed.add_field(
            name="📚 Library",
            value="discord.py",
            inline=True
        )
        
        embed.add_field(
            name="🌟 Features",
            value=(
                "• Summoner lookup & ranked stats\n"
                "• Match history & live games\n"
                "• Champion mastery & rotation\n"
                "• Player tracking & leaderboards\n"
                "• Champion builds & comparisons"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🔗 Links",
            value=(
                "[Riot Games API](https://developer.riotgames.com/)\n"
                "[Discord.py Docs](https://discordpy.readthedocs.io/)"
            ),
            inline=False
        )
        
        embed.add_field(
            name="⚖️ Legal",
            value=(
                "This bot is not endorsed by Riot Games and does not reflect "
                "the views or opinions of Riot Games or anyone officially "
                "involved in producing or managing Riot Games properties."
            ),
            inline=False
        )
        
        embed.set_footer(text="Made with ❤️ for the League of Legends community")
        
        await interaction.response.send_message(embed=embed)

