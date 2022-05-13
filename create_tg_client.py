import sys
import asyncio
from telethon import TelegramClient, events

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = sys.argv[1]
api_hash = sys.argv[2]

async def main():
  client = TelegramClient('tg_client', api_id, api_hash)
  await client.start()

asyncio.run(main())
