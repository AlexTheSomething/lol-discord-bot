"""
Clash command - Display upcoming Clash tournament information.
"""

import discord
from discord import app_commands
from discord.ext import commands
import riot_api
from utils.helpers import create_basic_embed, create_error_embed
import config
from datetime import datetime, timezone


async def setup(bot: commands.Bot):
    """Setup function to register the command with the bot."""
    
    @bot.tree.command(name="clash", description="Show upcoming Clash tournaments")
    async def clash(interaction: discord.Interaction):
        """
        Display upcoming Clash tournament schedules.
        
        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer()
        
        try:
            # Fetch clash tournaments
            tournaments = await riot_api.get_clash_tournaments(config.DEFAULT_REGION)
            
            if not tournaments:
                embed = create_basic_embed(
                    title="⚔️ Clash Tournaments",
                    description="No upcoming Clash tournaments scheduled at the moment.\n\n"
                               "Check back later or visit the League client for updates!"
                )
                embed.add_field(
                    name="Region",
                    value=config.DEFAULT_REGION.upper(),
                    inline=False
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Create main embed
            embed = create_basic_embed(
                title="⚔️ Upcoming Clash Tournaments",
                description=f"**{len(tournaments)} tournament(s)** scheduled for {config.DEFAULT_REGION.upper()}"
            )
            
            # Process each tournament
            for i, tournament in enumerate(tournaments[:3], 1):  # Show max 3 tournaments
                tournament_name = tournament.get("nameKey", "Unknown Tournament")
                tournament_id = tournament.get("id", "N/A")
                
                # Get tournament schedule
                schedule = tournament.get("schedule", [])
                
                if schedule:
                    # Format schedule dates
                    dates_text = []
                    for phase in schedule[:4]:  # Show max 4 phases
                        registration_time = phase.get("registrationTime", 0)
                        start_time = phase.get("startTime", 0)
                        
                        if start_time > 0:
                            # Convert from milliseconds to seconds
                            dt = datetime.fromtimestamp(start_time / 1000, tz=timezone.utc)
                            
                            # Format: "Jan 25 - 7:00 PM UTC"
                            date_str = dt.strftime("%b %d - %I:%M %p UTC")
                            dates_text.append(f"• {date_str}")
                    
                    schedule_display = "\n".join(dates_text) if dates_text else "Schedule TBA"
                else:
                    schedule_display = "Schedule not available"
                
                # Format tournament name (remove "CLASH_" prefix if present)
                display_name = tournament_name.replace("CLASH_", "").replace("_", " ").title()
                
                embed.add_field(
                    name=f"🏆 {display_name}",
                    value=schedule_display,
                    inline=False
                )
            
            embed.add_field(
                name="📝 How to Join",
                value=(
                    "1. Open League of Legends client\n"
                    "2. Click on Clash tab\n"
                    "3. Create or join a team\n"
                    "4. Register before the deadline!"
                ),
                inline=False
            )
            
            embed.set_footer(text="Times shown in UTC • Check client for your local time")
            
            await interaction.followup.send(embed=embed)
        
        except riot_api.RiotAPIError as e:
            embed = create_error_embed(str(e))
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = create_error_embed(f"An unexpected error occurred: {str(e)}")
            await interaction.followup.send(embed=embed)

