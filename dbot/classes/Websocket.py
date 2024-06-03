import os
import json
import websockets
import aiohttp
import asyncio


class Websocket:
    def __init__(self, bot):
        self.bot = bot
        self.api = os.getenv("api.url")
        self.websocket_url = os.getenv("websocket.url")
        self.api_key = os.getenv("api.key")

    async def websocket_listener(self):
        """
        Listen to WebSocket for real-time command updates
        """
        while True:
            try:
                async with websockets.connect(self.websocket_url) as websocket:
                    async for message in websocket:
                        data = json.loads(message)
                        if data.get("type") == "update_command":
                            guild_id = data.get("guild_id")
                            await self.update_commands_for_guild(guild_id)
                        elif data.get("type") == "update_prefix":
                            guild_id = data.get("guild_id")
                            await self.update_prefix_for_guild(guild_id)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed. Reconnecting...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Unexpected error: {e}")
                await asyncio.sleep(5)

    async def update_commands_for_guild(self, guild_id):
        """
        Update commands for a specific guild
        """
        url = f"{self.api}/guilds/{guild_id}/commands"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    commands = await response.json()
                else:
                    print(
                        f"Failed to fetch commands for guild {guild_id}: {response.status}"
                    )
                    return

        # Remove all existing commands for the guild
        guild = self.bot.get_guild(guild_id)
        if guild:
            for command in list(self.bot.commands):
                self.bot.remove_command(command.name)

            # Add new commands
            for command_data in commands:

                async def new_command(ctx, *args, command_data=command_data):
                    await ctx.send(command_data["response"])

                new_command.__name__ = command_data["trigger"]
                self.bot.command(name=command_data["trigger"])(new_command)

    async def update_prefix_for_guild(self, guild_id):
        """
        Update prefix for a specific guild
        """
        url = f"{self.api}/guilds/{guild_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    guild_data = await response.json()
                    prefix = guild_data["prefix"]
                    self.bot.command_prefix = prefix
                else:
                    print(
                        f"Failed to fetch guild data for guild {guild_id}: {response.status}"
                    )
