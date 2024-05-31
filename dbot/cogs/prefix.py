import nextcord, requests, asyncio, os
from nextcord.ext import commands
from aiohttp import web
from dbot.classes.api import Api


class Prefix(commands.Cog):
    def __init__(self, bot):
        """
        This class is used to set a custom prefix for the server.
        """
        self.client = bot
        self.api = Api()
        self.api = self.api.getUrl()
        if self.api == None:
            return False
        self.default_prefix = "!"

        self.start_prefix_webbook()

    def get_prefix(self, message):
        """
        This function is used to get the prefix for the server.
        It goes to the API route /get_prefix and gets the prefix for the server.
        """
        if isinstance(message.channel, nextcord.DMChannel):
            return self.default_prefix
        else:
            guild_id = message.guild.id
            r = requests.get(f"{self.api}/get_prefix?guildid={guild_id}")

            if r.status_code == 200:
                return r.json()["prefix"]
            else:
                return self.default_prefix

    @nextcord.slash_command(
        name="setprefix", description="Set a custom prefix for the server."
    )
    @commands.has_permissions(administrator=True)
    async def setprefix(self, interaction: nextcord.Interaction, prefix: str):
        """
        This function is used to set a custom prefix for the server.
        It goes to the API route /put_prefix and sets the prefix for the server.
        """
        guild_id = interaction.guild.id

        r = requests.put(f"{self.api}/put_prefix?guildid={guild_id}&prefix={prefix}")
        if r.status_code == 200:
            await interaction.response.send_message(f"Prefix set to {prefix}")
        else:
            await interaction.response.send_message(
                "An error occurred. Please contact support"
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        This function is used to set the default prefix for the server when the bot joins for the first time.
        It goes to the API route /post_prefix and sets the default prefix for the server.
        """
        guild_id = guild.id
        r = requests.post(
            f"{self.api}/post_prefix?guildid={guild_id}&prefix={self.default_prefix}"
        )

        if r.status_code != 200:
            print(
                f"An error occurred. No guild prefix set for {guild.name} - {guild.id}"
            )
        return r.status_code == 200

    ################
    # Webhook Code #
    ################
    def start_prefix_webhook(self):
        """
        This function is used to start the webhook for the prefix.
        It creates a web server using aiohttp and listens on the given port.
        When a POST request is made to /bot/webhook/prefix, it updates the prefix for the server.
        """
        app = web.Application()
        app.router.add_post("/bot/webhook/prefix", self.handle_webhook)

        runner = web.AppRunner(app)
        asyncio.get_event_loop().run_until_complete(runner.setup())
        webhook_url, webhook_port = os.getenv('webhook.url').split(':')
        site = web.TCPSite(runner, webhook_url, webhook_port)
        asyncio.get_event_loop().run_until_complete(site.start())

    async def handle_webhook(self, request):
        """
        This function is used to handle the POST request made to /bot/webhook/prefix.
        """
        data = await request.json()
        guild_id = data.get("guild_id")
        new_prefix = data.get("prefix")
        if guild_id and new_prefix:
            self.prefixes[guild_id] = new_prefix
            print(f"Prefix updated for guild {guild_id}: {new_prefix}")
            return web.Response(text="Prefix updated")
        return web.Response(status=400, text="Invalid data")


def setup(bot):
    bot.add_cog(Prefix(bot))
