import nextcord, requests
from nextcord.ext import commands
from dbot.classes.database import Database


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.db = Database.url()
        self.default_prefix = "!"

    def get_prefix(self, message):
        if isinstance(message.channel, nextcord.DMChannel):
            return self.default_prefix
        else:
            guild_id = message.guild.id
            r = requests.get(f"{self.db}/get_prefix?guildid={guild_id}")
            return r.json()["prefix"] if r.status_code == 200 else self.default_prefix

    @nextcord.ui.slash_command(
        name="setprefix", description="Set a custom prefix for the server."
    )
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: nextcord.ui.Context, prefix: str):
        guild_id = ctx.guild.id

        r = requests.put(f"{self.db}/put_prefix?guildid={guild_id}&prefix={prefix}")
        return await ctx.send(f"Prefix set to {prefix}") if r.status_code == 200 else await ctx.send("An error occurred. Please contact support")

    async def prefix_on_guild_join(self, guild):
        guild_id = guild.id
        r = requests.post(f"{self.db}/post_prefix?guildid={guild_id}&prefix={self.default_prefix}")
        return r.status_code == 200


def setup(bot):
    bot.add_cog(Prefix(bot))
