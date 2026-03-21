import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
USER_ID = os.getenv("DISCORD_ID")

HEADERS = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json",
}

def create_dm(user_id: str) -> str:
    r = requests.post(
        f"https://discord.com/api/v10/users/@me/channels",
        headers=HEADERS,
        json={"recipient_id": user_id},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["id"]

def send_dm(channel_id: str, text: str) -> None:
    r = requests.post(
        f"https://discord.com/api/v10/channels/{channel_id}/messages",
        headers=HEADERS,
        json={"content": text},
        timeout=10,
    )
    r.raise_for_status()

def send_notifier(user_id, msg):
    dm_channel_id = create_dm(user_id)
    send_dm(dm_channel_id, msg)
