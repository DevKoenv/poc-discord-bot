import nextcord

class BotHandling:
    async def join(self, interaction: nextcord.Interaction):
        """
        Joins a voice channel
        """
        if interaction.author.voice is None:
            await interaction.response.send("You are not in a voice channel.", ephemeral=True)
            return

        if interaction.guild.voice_client is not None:
            await interaction.response.send("I am already in a voice channel.", ephemeral=True)
            return

        await interaction.author.voice.channel.connect()
    
    async def leave(self, interaction: nextcord.Interaction):
        """
        Leaves a voice channel
        """
        if interaction.guild.voice_client is None:
            await interaction.response.send("I am not in a voice channel.", ephemeral=True)
            return

        if interaction.guild.voice_client.channel != interaction.author.voice.channel:
            await interaction.response.send("You are not in the same voice channel as me.", ephemeral=True)
            return

        await interaction.guild.voice_client.disconnect()