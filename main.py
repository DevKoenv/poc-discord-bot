from dbot.client import Client
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    await Client().setup()
    #start db
    
if __name__ == "__main__":
    asyncio.run(main())
