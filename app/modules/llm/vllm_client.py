import os
from typing import List
from modules.llm.llm_client import LLMClient
from modules.llm.types import Chat, Pal
from openai import OpenAI


class VLLMClient(LLMClient):
    def __init__(self):
        super().__init__()
        base_url = os.environ.get("TEXT_SERVER_URL")
        self.client = OpenAI(
            base_url=base_url,
            api_key="token-abc123",

        )

        self.model_name = "Qwen/Qwen2.5-7B-Instruct"

    def send(self, user_input: str, system: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            temperature=1.0,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_input}
            ]
        )
        return completion.choices[0].message.content

    def get_chat_response(self, chats: List[Chat], bot_name: str = None, bot_bg: str = None, writing_prompt: str = None) -> str:
        if bot_name is None or bot_bg is None or writing_prompt is None:
            raise ValueError("bot_name, bot_bg, and writing_prompt must be provided.")

        formatted_chats = (["1. User: Hi, can we talk about the essay topic? We can perhaps deep dive into the topic together?"] +
                           [f"{i + 2}. {bot_name}: {chat.content}" for i, chat in enumerate(chats)])
        prompt = f"# Task\n- Pretend that your are {bot_name}, respond to the chat based on the provided information.\n# {bot_name}'s Background\n- {bot_bg} \n\n# Rules\n- Only output {bot_name}'s response without any explanation.\n- Output format should be `<chat_round>. {bot_name}: <response>`\n- Be natural and simulate a real world chat.\n# Context\nYou are having a **deep dive** chat with \"User\" about the writing prompt - \"{writing_prompt}\"\nYou want to share how would you write a passage about the writing prompt, what you think about the writing prompt, or anything you want to share with the user about the writing prompt. Make use of your own knowledge and experience. Don't be afraid to make up your experience beyound the given background, be creative.\n# **Chat**\n{"\n".join(formatted_chats)}"
        return self.send(prompt, "You are a professional actor, who is good at role-playing different characters based on the provided background, at the same time, you strictly follows the restrictions.")


    def summarize_chat(self, chats: List[Chat], bot_name: str = None) -> str:
        if bot_name is None:
            raise ValueError("bot_name must be provided.")

        formatted_chats = (["1. User: Hi, can we talk about the essay topic? We can perhaps deep dive into the topic together?"] +
                           [f"{i + 2}. {bot_name}: {chat.content}" for i, chat in enumerate(chats)])
        prompt = "\n".join(formatted_chats) + "\n---\nWrite a summary for the above chat, focus on the result of the chat like what they've decided."
        return self.send(prompt, "You are a helpful linguistic, who is good at writing useful chat summaries.")

    def generate_pals(self, prompt: str) -> Pal:
        prompt = f"You are provided with the following essay prompt:\n\"{prompt}\"\n\nImagine someone who is interested in this essay topic, and create a character that relates to the topic. Provide both his **name**, and his **detailed** background.\nYou also need to explain why the character might be interested in the topic step-by-step, quote the essay prompt if needed."
        raw_pal = self.send(prompt, "You are a helpful character designer, who is good at creating characters with depth based on any information.")

        return Pal(name="John Doe", occupation="Writer", description="This is a hard coded PAL.")

    def get_language_suggestion(self, writing: str) -> str:
        prompt = f"# Student writing\n{writing}\n\n# Task\nGrade the language of the above student writing based on the following marking scheme, justify your markings.\n**Language (L)**\n\n* **Excellent (7-6 Marks):** Wide range of accurate and varied sentence structures, including complex sentences used effectively.  Grammar is accurate with minimal errors. Vocabulary is precise, sophisticated, and used effectively to convey nuances of meaning. Spelling and punctuation are accurate. Register, tone, and style are consistently appropriate to the genre and text type.\n* **Good (5 Marks):** A range of accurate sentence structures, with some attempts at complexity. Grammatical errors may occur in more complex structures but do not significantly impede clarity.  Vocabulary is moderately wide and used appropriately. Spelling and punctuation are generally accurate. Register, tone, and style are mostly appropriate.\n* **Fair (4 Marks):** Simple sentences are generally accurate, with occasional attempts at more complex structures.  Repetitive sentence structures and grammatical errors may sometimes affect meaning. Common vocabulary is generally appropriate. Basic spelling and punctuation are accurate. Some evidence of appropriate register, tone, and style.\n* **Weak (3 Marks):** Short, simple sentences are generally accurate, but attempts at complexity are limited and often unsuccessful. Grammatical errors frequently affect meaning. Vocabulary is simple and limited. Spelling of common words and basic punctuation are mostly accurate.\n* **Very Weak (2 Marks):** Some short, simple sentences are accurately structured, but grammatical errors frequently impact meaning.  Vocabulary is very simple and limited.  A few words are spelled correctly, and basic punctuation is occasionally accurate.\n* **Minimal (1 Mark):** Multiple errors in sentence structures, spelling, and word usage significantly impede understanding.\n* **Nonexistent (0 Marks):** Not enough language present to assess.\n# Output format\nLevel: <level>\nComments (Language): <comments about the language>"
        return self.send(prompt, "You are an English teacher who focus on Hong Kong Diploma of Secondary Education Exam, specifically, the English writing paper. You are good at writing useful suggestions for students.")

    def get_content_suggestion(self, writing: str) -> str:
        prompt = f"# Student writing\n{writing}\n\n# Task\nGrade the content of the above student writing based on the following marking scheme, justify your markings.\n**Content (C)**\n\n* **Excellent (7-6 Marks):** Fully addresses the question with complete relevance. Ideas are well-developed, supported, and demonstrate creativity and imagination where appropriate. Shows a strong awareness of the audience.\n* **Good (5 Marks):** Adequately addresses the question with mostly relevant content. Some ideas are well-developed and supported, showing creativity and imagination at times. Demonstrates some awareness of the audience.\n* **Fair (4 Marks):** Just satisfies the requirements with some relevant ideas, but may contain gaps or redundant information.  Development of ideas is limited, and creativity and imagination may be present but inconsistently. Shows occasional awareness of the audience.\n* **Weak (3 Marks):** Partially addresses the question with some relevant ideas, but significant gaps exist in understanding. Ideas are not well-developed, and there may be repetition.  Struggles to orient the reader effectively to the topic.\n* **Very Weak (2 Marks):** Shows very limited attempts to fulfill the requirements. Content is intermittently relevant with few developed ideas. May include misconceptions or inaccurate information. Very limited awareness of audience.\n* **Minimal (1 Mark):** Inadequate content heavily reliant on prompts. Few ideas are present, and none are developed.  Content may be copied from prompts or reading texts. Almost total lack of awareness of audience.\n* **Nonexistent (0 Marks):** Totally inadequate, irrelevant, or memorized content copied directly from prompts or reading texts. No awareness of audience.\n# Output format\nLevel: <level>\nComments (Content): <comments about the content>"

        return self.send(prompt, "You are an English teacher who focus on Hong Kong Diploma of Secondary Education Exam, specifically, the English writing paper. You are good at writing useful suggestions for students.")

    def get_organization_suggestion(self, writing: str) -> str:
        prompt = f"# Student writing\n{writing}\n\n# Task\nGrade the organization of the above student writing based on the following marking scheme, justify your markings.\n**Organization (O)**\n\n* **Excellent (7-6 Marks):** Text is highly organized and effectively structured with a clear and logical progression of ideas.  Cohesion is seamless and sophisticated, using a variety of cohesive devices. Overall structure is coherent, sophisticated, and perfectly suited to the genre and text type.\n* **Good (5 Marks):** Text is well-organized with a logical development of ideas.  Cohesion is clear and effective, using strong cohesive ties.  Overall structure is coherent, sophisticated, and appropriate to the genre and text type.\n* **Fair (4 Marks):** Parts of the text have clearly defined topics. Cohesion is present in some parts, but may be inconsistent. Some cohesive ties are used.  Overall structure is mostly coherent and generally appropriate to the genre and text type.\n* **Weak (3 Marks):** The text shows some attempt at organization, but the structure may be unclear or illogical. Simple cohesive ties are used inconsistently, and cohesion is often fuzzy. A limited range of cohesive devices is used.\n* **Very Weak (2 Marks):** Some attempts are made to organize the text, but the connection between ideas is often weak. Cohesive devices are used sparingly and may be ineffective.\n* **Minimal (1 Mark):** A minimal attempt is made to organize the text, but the structure is largely unclear. Very limited use of cohesive devices.\n* **Nonexistent (0 Marks):** Text lacks any discernible organization.  Words, phrases, or sentences are disconnected. Cohesive devices are almost entirely absent.\n# Output format\nLevel: <level>\nComments (Organization): <comments about the organization>"
        return self.send(prompt, "You are an English teacher who focus on Hong Kong Diploma of Secondary Education Exam, specifically, the English writing paper. You are good at writing useful suggestions for students.")