import requests as req, os

class Api:
    def __init__(self):
        self.url = os.getenv('api.url')

    def checkConnection(self):
        """
        Check if the API is reachable
        :return: True if the API is reachable, False otherwise
        """
        status = req.get(self.url).status_code
        return True if status == 200 else False

    def getUrl(self):
        """
        Get the API URL
        :return: The API URL if the API is reachable, None otherwise
        """
        return self.url if self.checkConnection() else None