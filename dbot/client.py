import os, nextcord
from nextcord.ext import commands
from dbot.cogs.prefix import Prefix


class Client:
    def __init__(self):
        """
        Initialization for the Discord Bot
        """
        self.client = commands.Bot(
            command_prefix=Prefix().get_prefix,
            intents=nextcord.Intents.all(),
            owner_ids=[int(i) for i in os.getenv("bot.ownerids").split(",")],
            case_insensitive=True,
            help_command=None,
        )

    async def setup(self):
        """
        Setup the discord bot
        """
        os.system("cls" if os.name == "nt" else "clear")
        print("Starting bot...")
        self.client.add_listener(self.on_ready)
        await self.loadCogs()
        await self.run()

    async def loadCogs(self):
        """
        Load all cogs
        """
        for root, _, files in os.walk('./dbot/cogs'):
            for filename in files:
                if filename.endswith('.py'):
                    try:
                        path = os.path.join(root, filename)[len("./dbot/cogs/"):][:-3].replace(os.path.sep, '.')
                        self.client.load_extension(f'dbot.cogs.{path}')
                        print(f"Loaded cog: {filename[:-3]}")
                    except Exception as e:
                        print(f"Error loading cog {filename[:-3]}: {e}")


    async def run(self):
        """
        Run the discord bot using the token from environment variables
        """
        await self.client.start(os.getenv("bot.token"))

    async def on_ready(self):
        """
        Function to execute when bot is ready
        """
        print(
            f"""

Logged in as:       {self.client.user}
ID:                 {self.client.user.id}
Prefix:             {self.client.command_prefix}
Guilds:             {len(self.client.guilds)}
Total members:      {len(self.client.users)}
Cogs Loaded:        {len(self.client.cogs)}
Commands:           {len(self.client.get_all_application_commands())}

Bot is ready!
"""
        )
