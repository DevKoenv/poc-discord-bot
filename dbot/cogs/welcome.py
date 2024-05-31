import nextcord, os
from nextcord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        This event is triggered when the bot joins a guild.
        The bot sends a welcome message to the owner of the guild or the bot inviter.
        """
        welcomeEmbed = nextcord.Embed(
            title=f"👋 Thanks for using {self.client.user.name}!",
            description=f"In order to manage your server on the web dashboard, follow [this link]({os.getenv('dashboard.url')}).",
            color=nextcord.Color.green(),
        )

        owner = guild.owner
        bot_inviter = None

        integrations = await guild.integrations()   
        for integration in integrations:
            if (
                isinstance(integration, nextcord.Integration)
                and integration.type == nextcord.IntegrationType.bot
            ):
                if integration.application.name == self.client.user.name:
                    bot_inviter = integration.user
                    break

        if bot_inviter is not None and bot_inviter.id != owner.id:
            await bot_inviter.send(embed=welcomeEmbed)
        await owner.send(embed=welcomeEmbed)

def setup(bot):
    bot.add_cog(Welcome(bot))
