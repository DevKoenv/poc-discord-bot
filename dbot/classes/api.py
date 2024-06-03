import os, requests as req

class Api:
    def __init__(self):
        self.url = os.getenv("api.url")

    def getUrl(self):
        """
        Get the URL for the bot's dashboard
        """
        return self.url
    
    def getPrefix(self, guild_id):
        """
        Request: GET
        Get the prefix for the server
        Args: guild_id (int)
        """
        return f"{self.url}/{guild_id}/get_prefix"
    
    def setPrefix(self, guild_id, prefix):
        """
        Request: POST
        Set the prefix for the server
        Args: guild_id (int), prefix (str)
        """
        return f"{self.url}/{guild_id}/set_prefix/{prefix}"