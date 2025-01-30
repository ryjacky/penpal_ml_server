import asyncio
import os
import ssl

from realtime import AsyncRealtimeChannel, AsyncRealtimeClient

from modules.worker.utils import insert_message, is_bot



def postgres_changes_callback(payload, *args):
    print("*: ", payload)


def postgres_changes_insert_callback(payload, *args):
    print("INSERT: ", payload)


def postgres_changes_delete_callback(payload, *args):
    print("DELETE: ", payload)


def postgres_changes_update_callback(payload, *args):
    inbox_id = payload["data"]["record"]["id"]
    user_id = is_bot(inbox_id)
    if user_id:
        insert_message(inbox_id, user_id)
    print("UPDATE: ", payload)


async def test_postgres_changes(socket: AsyncRealtimeClient):
    await socket.connect()

    # Add your access token here
    # await socket.set_auth("ACCESS_TOKEN")

    channel = socket.channel("test-postgres-changes")

    await channel.on_postgres_changes(

        "UPDATE", table="inbox", callback=postgres_changes_update_callback
    ).subscribe()

    await socket.listen()


async def chatbot_worker():
    URL = os.getenv("SUPABASE_URL")
    JWT = os.getenv("SUPABASE_KEY")

    # Setup the broadcast socket and channel
    socket = AsyncRealtimeClient(f"{URL}/realtime/v1", JWT, auto_reconnect=True)
    ssl._create_default_https_context = ssl._create_unverified_context()
    await socket.connect()

    await test_postgres_changes(socket)

