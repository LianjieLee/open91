import os
import sys

import requests
from faker import Faker
from telethon import TelegramClient, sync

# https://docs.telethon.dev/en/latest/concepts/sessions.html
# sync can not omit
def send_video(api_id, api_hash, peer_name, filepath, caption, thumb):
    client = TelegramClient("tg_client", api_id, api_hash)
    client.start()
    client.connect()
    pic = requests.get(thumb, headers={'User-Agent': Faker().user_agent()}).content
    client.send_file(peer_name, filepath, caption=caption, thumb=pic, supports_streaming=True)

if __name__ == '__main__':
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    peer_name = sys.argv[1]
    filepath = sys.argv[2]
    caption = sys.argv[3]
    thumb = sys.argv[4]
    send_video(api_id, api_hash, peer_name, filepath, caption, thumb)
