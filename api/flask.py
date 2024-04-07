import os, flask

class Flask():
    def __init__(self, client):
        self.client = client
        self.port = os.getenv('flask.port')
        self.dev = os.getenv('dev.enabled') 
        print(self.client)