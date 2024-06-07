import nextcord

class MusicHandling:
    async def checkVoiceCall(self, interaction: nextcord.Interaction):
        if interaction.guild.voice_client is None:
            await interaction.response.send("I am not in a voice channel.", ephemeral=True)
            return False

        if interaction.guild.voice_client.channel != interaction.author.voice.channel:
            await interaction.response.send("You are not in the same voice channel as me.", ephemeral=True)
            return False
        
        return True

    async def play(self, interaction: nextcord.Interaction):
        """
        Plays a song
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement play command
        pass

    async def pause(self, interaction: nextcord.Interaction):
        """
        Pauses the current song
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement pause command
        pass

    async def resume(self, interaction: nextcord.Interaction):
        """
        Resumes the current song
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement resume command
        pass

    async def stop(self, interaction: nextcord.Interaction):
        """
        Stops the current song
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement stop command
        pass

    async def skip(self, interaction: nextcord.Interaction):
        """
        Skips the current song
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement skip command
        pass

    async def queue(self, interaction: nextcord.Interaction):
        """
        Shows the current queue
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement queue command
        pass

    async def clear(self, interaction: nextcord.Interaction):
        """
        Clears the current queue
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement clear command
        pass

    async def loop(self, interaction: nextcord.Interaction):
        """
        Loops the current song
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement loop command
        pass

    async def shuffle(self, interaction: nextcord.Interaction):
        """
        Shuffles the current queue
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement shuffle command
        pass

    async def remove(self, interaction: nextcord.Interaction):
        """
        Removes a song from the queue
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement remove command
        pass

    async def lyrics(self, interaction: nextcord.Interaction):
        """
        Shows the lyrics of the current song
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement lyrics command
        pass

    async def playnext(self, interaction: nextcord.Interaction):
        """
        Plays a song next
        """
        if not await self.checkVoiceCall(interaction):
            return
        
        #TODO: Implement playnext command
        pass