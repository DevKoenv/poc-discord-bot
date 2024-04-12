import nextcord
from nextcord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    async def welcome_on_guild_join(self, guild):
        welcomeEmbed = nextcord.Embed(
            title=f"Welcome to {self.client.user.name}!",
            description="Thanks for inviting me.",
            color=nextcord.Color.green(),
        )

        owner = guild.owner
        bot_inviter = None

        integrations = await guild.fetch_integrations()
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
