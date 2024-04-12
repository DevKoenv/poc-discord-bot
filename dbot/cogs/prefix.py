import nextcord
from nextcord.ext import commands
from dbot.classes.database import Database


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.db = Database().getConn()
        self.cursor = Database().getCursor()

    def get_prefix(self, message):
        default_prefix = "!"
        if isinstance(message.channel, nextcord.DMChannel):
            return default_prefix
        else:
            guild_id = message.guild.id
            self.cursor.execute("SELECT prefix FROM prefixes WHERE guild_id=?", (guild_id,))
            result = self.cursor.fetchone()
            return result[0] if result else default_prefix

    @nextcord.ui.slash_command(name="setprefix", description="Set a custom prefix for the server.")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: nextcord.ui.Context, prefix: str):
        guild_id = ctx.guild.id
        self.cursor.execute(
            "REPLACE INTO prefixes (guild_id, prefix) VALUES (?, ?)", (guild_id, prefix)
        )
        self.db.commit()
        await ctx.send(f"Prefix set to {prefix}")

    async def on_guild_join(self, guild):
        self.cursor.execute("INSERT INTO prefixes (guild_id, prefix) VALUES (?, ?)", (guild.id, "!"))
        self.db.commit()

def setup(bot):
    bot.add_cog(Prefix(bot))