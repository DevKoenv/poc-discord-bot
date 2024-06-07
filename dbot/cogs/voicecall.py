import nextcord, requests as req, os
from nextcord.ext import commands
from dbot.classes.voicecall.BotHandling import BotHandling
from dbot.classes.voicecall.MusicHandling import MusicHandling


class VoiceCall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botHandling = BotHandling()
        self.musicHandling = MusicHandling()
        self.enabledMusicPlay = None

    def checkMusicPlay(self):
        if self.enabledMusicPlay is None:
            # TODO: Check if the bot is allowed to play music with API
            self.enabledMusicPlay = True
        return self.enabledMusicPlay

    @nextcord.slash_command(name="join", description="Joins a voice channel")
    async def join(self, interaction: nextcord.Interaction):
        """
        Joins a voice channel
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.botHandling.join(interaction)

    @nextcord.slash_command(name="leave", description="Leaves a voice channel")
    async def leave(self, interaction: nextcord.Interaction):
        """
        Leaves a voice channel
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.botHandling.leave(interaction)

    @nextcord.slash_command(name="play", description="Plays a song")
    async def play(self, interaction: nextcord.Interaction):
        """
        Plays a song
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.play(interaction)

    @nextcord.slash_command(name="pause", description="Pauses the current song")
    async def pause(self, interaction: nextcord.Interaction):
        """
        Pauses the current song
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.pause(interaction)

    @nextcord.slash_command(name="resume", description="Resumes the current song")
    async def resume(self, interaction: nextcord.Interaction):
        """
        Resumes the current song
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.resume(interaction)

    @nextcord.slash_command(name="stop", description="Stops the current song")
    async def stop(self, interaction: nextcord.Interaction):
        """
        Stops the current song
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.stop(interaction)

    @nextcord.slash_command(name="skip", description="Skips the current song")
    async def skip(self, interaction: nextcord.Interaction):
        """
        Skips the current song
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.skip(interaction)

    @nextcord.slash_command(name="queue", description="Shows the current queue")
    async def queue(self, interaction: nextcord.Interaction):
        """
        Shows the current queue
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.queue(interaction)

    @nextcord.slash_command(name="clear", description="Clears the current queue")
    async def clear(self, interaction: nextcord.Interaction):
        """
        Clears the current queue
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.clear(interaction)

    @nextcord.slash_command(name="loop", description="Loops the current song")
    async def loop(self, interaction: nextcord.Interaction):
        """
        Loops the current song
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.loop(interaction)

    @nextcord.slash_command(name="shuffle", description="Shuffles the current queue")
    async def shuffle(self, interaction: nextcord.Interaction):
        """
        Shuffles the current queue
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.shuffle(interaction)

    @nextcord.slash_command(name="remove", description="Removes a song from the queue")
    async def remove(self, interaction: nextcord.Interaction):
        """
        Removes a song from the queue
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.remove(interaction)

    @nextcord.slash_command(
        name="lyrics", description="Shows the lyrics of the current song"
    )
    async def lyrics(self, interaction: nextcord.Interaction):
        """
        Shows the lyrics of the current song
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.lyrics(interaction)

    @nextcord.slash_command(
        name="playnext", description="Plays a song next in the queue"
    )
    async def playnext(self, interaction: nextcord.Interaction):
        """
        Plays a song next in the queue
        """
        if self.enabledMusicPlay is None:
            self.checkMusicPlay()
        if self.enabledMusicPlay is False:
            await interaction.response.send(
                f"Voice feature is disabled. Go to the [dashboard]({os.getenv('dashboard.url')})"
            )
            return
        await self.musicHandling.playnext(interaction)


def setup(bot):
    bot.add_cog(VoiceCall(bot))
