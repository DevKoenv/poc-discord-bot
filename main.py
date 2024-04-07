# Custom classes
from api.flask import Flask
from dbot.client import Client

################################################################
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    client = Client()
    await client.setup()
    exit()
    Flask(client)


if __name__ == "__main__":
    asyncio.run(main())
