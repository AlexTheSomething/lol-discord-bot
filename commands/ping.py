"""
Ping command - Display bot latency.
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import create_basic_embed


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="ping", description="Check bot latency")
    async def ping(interaction: discord.Interaction):
        """
        Display bot latency in milliseconds.
        
        Args:
            interaction: Discord interaction
        """
        # Calculate latency
        latency = round(bot.latency * 1000, 2)
        
        # Determine status emoji based on latency
        if latency < 100:
            status = "🟢 Excellent"
        elif latency < 200:
            status = "🟡 Good"
        elif latency < 300:
            status = "🟠 Fair"
        else:
            status = "🔴 Poor"
        
        embed = create_basic_embed(
            title="🏓 Pong!",
            description=f"**Latency:** {latency}ms\n**Status:** {status}"
        )
        
        await interaction.response.send_message(embed=embed)

