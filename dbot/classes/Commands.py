import os
import json
import websockets
import aiohttp

class Commands:
    def __init__(self, bot):
        self.bot = bot
        self.websocket_url = os.getenv("websocket.url")

    async def websocket_listener(self):
        """
        Listen to WebSocket for real-time command updates
        """
        async with websockets.connect(self.websocket_url) as websocket:
            async for message in websocket:
                data = json.loads(message)
                if data.get('type') == "update_command":
                    guild_id = data.get('guild_id')
                    await self.update_commands_for_guild(guild_id)

    async def update_commands_for_guild(self, guild_id):
        """
        Update commands for a specific guild
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{os.getenv("api.url")}/commands/{guild_id}') as response:
                commands = await response.json()

        # Remove all existing commands for the guild
        guild = self.bot.get_guild(guild_id)
        if guild:
            for command in self.bot.commands:
                self.bot.remove_command(command.name)

            # Add new commands
            for command_data in commands:
                async def new_command(ctx, *args):
                    await ctx.send(command_data['response'])
                new_command.__name__ = command_data['name']
                self.bot.command(name=command_data['name'])(new_command)
