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

def get_journey_info(journey_id):
    return clients.supabase_client.table("journey").select("id, essay_title, chatbot_name, chatbot_description, summaries").eq("id", journey_id).execute().data[0]

def insert_message(journey_id, user_id):
    journey_chats: list[Chat] = get_chats(journey_id)
    journey_info = get_journey_info(journey_id)
    if journey_info["summaries"] is not None:
        print("The chat has completed, not generating new replies.")
        return

    if journey_chats[-1].content == "/end":
        create_summary(journey_id, journey_chats, journey_info["chatbot_name"])
        return

    response: str = clients.chat_client.get_chat_response(journey_chats, bot_name=journey_info["chatbot_name"], bot_bg=journey_info["chatbot_description"], writing_prompt=journey_info["essay_title"])
    if response is None:
        print("Response is None, not inserting new messages!")
        return

    response = response.split(":", 1)[-1].strip()

    new_message = {"journey_id": journey_id, "content": response, "is_from_user": False, "user_id": user_id}
    clients.supabase_client.table("journey_messages").insert(new_message).execute()

    print("New message inserted.")


def create_summary(journey_id, journey_chats: list[Chat], bot_name):
    clients.supabase_client.table("journey").update({"summaries": "Generating summaries..."}).eq("id", journey_id).execute()
    response = clients.chat_client.summarize_chat(journey_chats, bot_name=bot_name)
    if response is None:
        print("Response is None, not inserting new summary!")
        return
    clients.supabase_client.table("journey").update({"summaries": response}).eq("id", journey_id).execute()