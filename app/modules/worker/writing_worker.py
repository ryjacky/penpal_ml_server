# Modified from https://github.com/supabase/realtime-py/blob/v2.2.0/example/app.py

import asyncio
import ssl
from concurrent.futures import ThreadPoolExecutor

from realtime import AsyncRealtimeChannel, AsyncRealtimeClient

from modules.worker.utils import get_message, get_chats, insert_message
import clients as clients
import os

from modules.worker.types import JourneyMessage

from modules.worker.utils import get_journey_info


def on_writing_inserted(payload, *args):
    print("INSERT: ", payload)
    content = payload["data"]["record"]["content"]
    writing_id = payload["data"]["record"]["id"]
    journey_info = get_journey_info(payload["data"]["record"]["owner_journey_id"])

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(clients.chat_client.get_language_suggestion, content, journey_info["essay_title"]),
                   executor.submit(clients.chat_client.get_organization_suggestion, content, journey_info["essay_title"]),
                   executor.submit(clients.chat_client.get_content_suggestion, content, journey_info["essay_title"]),
                   ]

        response = [future.result() for future in futures]

        lang: str = response[0].split("Comments (Language):")
        org: str = response[1].split("Comments (Organization):")
        content: str = response[2].split("Comments (Content):")

    try:
        clients.supabase_client.table("uploaded_writings").update({
            "content_comments": content[1].strip(),
            "language_comments": lang[1].strip(),
            "organization_comments": org[1].strip(),
            "generated_content_mark": content[0].replace("Level:", "").replace("5-7", "5").strip(),
            "generated_organization_mark": org[0].replace("Level:", "").replace("5-7", "5").strip(),
            "generated_language_mark": lang[0].replace("Level:", "").replace("5-7", "5").strip(),
        }).eq("id", writing_id).execute()
    except:
        clients.supabase_client.table("uploaded_writings").update({
            "content_comments": "FAILED",
            "language_comments": "FAILED",
            "organization_comments": "FAILED",
            "generated_content_mark": 0,
            "generated_organization_mark": 0,
            "generated_language_mark": 0,
        }).eq("id", writing_id).execute()


async def listen_for_new_writings(socket: AsyncRealtimeClient):
    await socket.connect()

    # Add your access token here
    # await socket.set_auth("ACCESS_TOKEN")

    channel = socket.channel("listen_for_new_writings")

    await channel.on_postgres_changes(
        "INSERT", table="uploaded_writings", callback=on_writing_inserted
    ).subscribe()

    await socket.listen()


async def writing_worker():
    URL = os.getenv("SUPABASE_URL")
    JWT = os.getenv("SUPABASE_KEY")

    # Setup the broadcast socket and channel
    socket = AsyncRealtimeClient(f"{URL}/realtime/v1", JWT, auto_reconnect=True)
    ssl._create_default_https_context = ssl._create_unverified_context()
    print("Writing worker is up and running")

    await socket.connect()

    await listen_for_new_writings(socket)

    # Cleanup
    await socket.remove_all_channels()
