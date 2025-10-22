"""
Main Discord bot file for the League of Legends Riot API Bot.
Initializes the bot and auto-loads all commands from the commands folder.
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import sys
import importlib.util
import config


class RiotBot(commands.Bot):
    """Custom bot class that extends commands.Bot."""
    
    def __init__(self):
        """Initialize the bot with required intents."""
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(command_prefix="!", intents=intents)
        # Note: self.tree is already created by commands.Bot, no need to create it again
    
    async def setup_hook(self):
        """
        Setup hook called when bot is starting up.
        This is where we load all commands.
        """
        print("Loading commands...")
        await self.load_commands()
        
        # Sync commands with Discord
        print("Syncing commands with Discord...")
        await self.tree.sync()
        print("Commands synced successfully!")
    
    async def load_commands(self):
        """
        Dynamically load all command files from the commands folder.
        Each command file should define a setup() function.
        """
        commands_dir = "commands"
        
        # Check if commands directory exists
        if not os.path.exists(commands_dir):
            print(f"Warning: {commands_dir} directory not found!")
            return
        
        # Get all Python files in commands directory
        command_files = [f for f in os.listdir(commands_dir) if f.endswith(".py") and not f.startswith("__")]
        
        for filename in command_files:
            command_name = filename[:-3]  # Remove .py extension
            module_path = os.path.join(commands_dir, filename)
            
            try:
                # Load the module dynamically
                spec = importlib.util.spec_from_file_location(command_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Call the setup function if it exists
                if hasattr(module, "setup"):
                    await module.setup(self)
                    print(f"✓ Loaded command: {command_name}")
                else:
                    print(f"⚠ Warning: {filename} has no setup() function")
            
            except Exception as e:
                print(f"✗ Failed to load {filename}: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready and connected to Discord."""
        print(f"\n{'='*50}")
        print(f"Bot is online and ready!")
        print(f"Logged in as: {self.user.name} (ID: {self.user.id})")
        print(f"{'='*50}\n")
        
        # Start the monitoring task
        if not self.monitor_stalked_players.is_running():
            self.monitor_stalked_players.start()
            print("✓ Player monitoring task started (checks every 2 minutes)\n")
    
    @tasks.loop(minutes=2)
    async def monitor_stalked_players(self):
        """Background task that monitors stalked players every 2 minutes."""
        try:
            # Import here to avoid circular imports
            from commands.track import monitor_players
            await monitor_players(self)
        except Exception as e:
            print(f"Error in monitoring task: {e}")
    
    @monitor_stalked_players.before_loop
    async def before_monitoring(self):
        """Wait until the bot is ready before starting monitoring."""
        await self.wait_until_ready()
    
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
        
        print(f"Command error: {error}")


async def main():
    """Main function to run the bot."""
    # Check if tokens are configured
    if config.DISCORD_TOKEN == "your_discord_token_here":
        print("❌ Error: DISCORD_TOKEN not configured!")
        print("Please set your Discord token in the .env file")
        sys.exit(1)
    
    if config.RIOT_API_KEY == "your_riot_api_key_here":
        print("❌ Error: RIOT_API_KEY not configured!")
        print("Please set your Riot API key in the .env file")
        sys.exit(1)
    
    # Create and run the bot
    bot = RiotBot()
    
    try:
        await bot.start(config.DISCORD_TOKEN)
    except discord.LoginFailure:
        print("❌ Error: Invalid Discord token!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import asyncio
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot shutting down...")

