# Modified from https://github.com/supabase/realtime-py/blob/v2.2.0/example/app.py

import asyncio
import ssl

from realtime import AsyncRealtimeChannel, AsyncRealtimeClient

from modules.worker.utils import get_message, get_chats, insert_message
import clients as clients
import os

from modules.worker.types import JourneyMessage

def postgres_changes_callback(payload, *args):
    print("*: ", payload)


def postgres_changes_insert_callback(payload, *args):
    print("INSERT: ", payload)
    journey_message_id = payload["data"]["record"]["id"]
    message: JourneyMessage = get_message(journey_message_id)
    if message.is_from_user:
        insert_message(message.journey_id, message.user_id)
        print("New message inserted.")


def postgres_changes_delete_callback(payload, *args):
    print("DELETE: ", payload)


def postgres_changes_update_callback(payload, *args):
    print("UPDATE: ", payload)


async def test_postgres_changes(socket: AsyncRealtimeClient):
    await socket.connect()

    # Add your access token here
    # await socket.set_auth("ACCESS_TOKEN")

    channel = socket.channel("test-postgres-changes")

    await channel.on_postgres_changes(
        "INSERT", table="journey_messages", callback=postgres_changes_insert_callback
    ).subscribe()

    await socket.listen()


async def chatbot_worker():

    URL = os.getenv("SUPABASE_URL")
    JWT = os.getenv("SUPABASE_KEY")

    # Setup the broadcast socket and channel
    socket = AsyncRealtimeClient(f"{URL}/realtime/v1", JWT, auto_reconnect=True)
    ssl._create_default_https_context = ssl._create_unverified_context()
    print("Chatbot worker is up and running")

    await socket.connect()

    await test_postgres_changes(socket)

    # Cleanup
    await socket.remove_all_channels()
