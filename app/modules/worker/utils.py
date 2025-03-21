from supabase import Client
from modules.llm.types import Chat
from modules.llm.llm_client import LLMClient
from modules.worker.types import JourneyMessage
import clients as clients

def get_message(journey_messages_id) -> JourneyMessage:
    message = clients.supabase_client.table("journey_messages").select("*").eq("id", journey_messages_id).execute().data[0]
    return JourneyMessage(
        journey_id=message["journey_id"],
        content=message["content"],
        is_from_user=message["is_from_user"],
        user_id=message["user_id"])

def get_chats(journey_id) -> list[Chat]:
    journey_messages = clients.supabase_client.table("journey_messages").select("*").eq("journey_id", journey_id).execute().data
    sorted_journey_messages = sorted(journey_messages, key=lambda x: x["id"])
    chats: list[Chat] = []
    for message in sorted_journey_messages:
        if message['is_from_user']:
            chat = Chat(role='user', content=message['content'])
            chats.append(chat)
        else:
            chat = Chat(role='assistant', content=message['content'])
            chats.append(chat)
    return chats

def insert_message(journey_id, user_id, client: LLMClient):
    journey_chats = get_chats(journey_id)
    response = client.get_chat_response(journey_chats)
    new_message = {"journey_id": journey_id, "content": response, "is_from_user": False, "user_id": user_id}
    clients.supabase_client.table("journey_messages").insert(new_message).execute()