from supabase import create_client, Client

from modules.llm.types import Chat
from modules.llm.llm_client import LLMClient

URL = os.getenv("SUPABASE_URL")
JWT = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(URL, JWT)


def get_message(journey_messages_id):
    message = supabase.table("journey_messages").select("*").eq("id", journey_messages_id).execute().data[0]
    journey_id = message["journey_id"]
    content = message["content"]
    is_from_user = message["is_from_user"]
    user_id = message["user_id"]
    return journey_id, content, is_from_user, user_id


def get_chats(journey_id):
    journey_messages = supabase.table("journey_messages").select("*").eq("journey_id", journey_id).execute().data
    sorted_journey_messages = sorted(journey_messages, key=lambda x: x["id"])
    chats = []
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
    supabase.table("journey_messages").insert(new_message).execute()
