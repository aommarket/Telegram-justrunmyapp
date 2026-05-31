import os
import re
from telethon import TelegramClient, events

# Environment variables
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

SOURCE_CHANNELS = [
    os.environ["SOURCE_CHANNEL_1"],
    os.environ["SOURCE_CHANNEL_2"]
]

TARGET_CHANNEL = os.environ["TARGET_CHANNEL"]

client = TelegramClient(
    "session",
    API_ID,
    API_HASH
)

def clean_text(text):
    if not text:
        return ""

    # Replace leverage with Spot
    text = re.sub(
        r'Leverage\s*:?\s*\d+\s*-\s*\d+x',
        'Spot',
        text,
        flags=re.IGNORECASE
    )

    return text.strip()

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    text = clean_text(event.raw_text or "")

    if text:
        await client.send_message(
            TARGET_CHANNEL,
            text
        )

async def main():
    print("Forward bot started...")
    await client.run_until_disconnected()

client.start()
client.loop.run_until_complete(main())
