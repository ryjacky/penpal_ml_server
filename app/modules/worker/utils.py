import os

from supabase import create_client, Client

URL = os.getenv("SUPABASE_URL")
JWT = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(URL, JWT)

def is_bot(inbox_id):
    user_id1 = supabase.table("inbox_participants").select("user_id_1").eq("inbox_id", inbox_id).execute().data[0]["user_id_1"]
    user_id2 = supabase.table("inbox_participants").select("user_id_2").eq("inbox_id", inbox_id).execute().data[0]["user_id_2"]
    for user_id in [user_id1, user_id2]:
        bot_user = supabase.table("bot_users").select("*").eq("user_id", user_id).execute().data
        if bot_user:
            print(f"The updated inbox is an inbox with a bot. {user_id} is the bot user.")
            return user_id
    print("The updated inbox is not an inbox with a bot.")
    return None

def insert_message(inbox_id, user_id):
    message = {"inbox_id": inbox_id, "content": "I am a bot.", "from_user_id": user_id}
    supabase.table("messages").insert(message).execute()
