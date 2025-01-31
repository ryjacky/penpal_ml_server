from typing import List, Literal
from modules.llm.llm_client import LLMClient
from modules.llm.types import Chat

from openai import OpenAI

class VLLMClient(LLMClient):
    model = "NousResearch/Meta-Llama-3-8B-Instruct"
    generate_pal_sys = """You are a helpful character designer, who is good at creating characters with depth based on any information."""
    generate_pal_prompt = """You are provided with the following essay prompt:
"{essay_prompt}"

Imagine someone who is interested in this essay topic, and create a character that relates to the topic. Provide both his **name**, and his **detailed** background.
You also need to explain why the character might be interested in the topic step-by-step, quote the essay prompt if needed."""

    summarize_chat_sys = """You are a helpful linguistic, who is good at writing useful chat summaries."""
    summarize_chat_prompt = """Generate a summary of the following conversation in first person view:
{chat_hist}"""

    chat_response_sys = "You are a professional actor, who is good at role-playing different characters based on the provided background, at the same time, you strictly follows the restrictions."
    chat_response_prompt = """# Task
- Pretend that your are {name}, respond to the chat based on the provided information.
# {name}'s Background
- {background}

# Rules
- Only output {name}'s response without any explanation.
- Output format should be `<chat_round>. {name}: <response>`
- Be natural and simulate a real world chat.
# Context
You are having a **deep dive** chat with "User" about the writing prompt - "{writing_prompt}"
You want to share how would you write a passage about the writing prompt, what you think about the writing prompt, or anything you want to share with the user about the writing prompt. Make use of your own knowledge and experience. Don't be afraid to make up your experience beyound the given background, be creative.
# **Chat**
{chat_hist}
"""
    writing_suggestion_sys = """You are an English teacher who focus on Hong Kong Diploma of Secondary Education Exam, specifically, the English writing paper. You are good at writing useful suggestions for students."""
    writing_suggestion_prompt = """# Student writing
{writing}

# Task
{writing_suggestion_prompt}
# Output format
Level: <level>
Comments (Language): <comments about the language>"""
    writing_rubrics = {
        "language": """Grade the language of the above student writing based on the following marking scheme, justify your markings.
**Language (L)**

* **Excellent (7-6 Marks):** Wide range of accurate and varied sentence structures, including complex sentences used effectively.  Grammar is accurate with minimal errors. Vocabulary is precise, sophisticated, and used effectively to convey nuances of meaning. Spelling and punctuation are accurate. Register, tone, and style are consistently appropriate to the genre and text type.
* **Good (5 Marks):** A range of accurate sentence structures, with some attempts at complexity. Grammatical errors may occur in more complex structures but do not significantly impede clarity.  Vocabulary is moderately wide and used appropriately. Spelling and punctuation are generally accurate. Register, tone, and style are mostly appropriate.
* **Fair (4 Marks):** Simple sentences are generally accurate, with occasional attempts at more complex structures.  Repetitive sentence structures and grammatical errors may sometimes affect meaning. Common vocabulary is generally appropriate. Basic spelling and punctuation are accurate. Some evidence of appropriate register, tone, and style.
* **Weak (3 Marks):** Short, simple sentences are generally accurate, but attempts at complexity are limited and often unsuccessful. Grammatical errors frequently affect meaning. Vocabulary is simple and limited. Spelling of common words and basic punctuation are mostly accurate.
* **Very Weak (2 Marks):** Some short, simple sentences are accurately structured, but grammatical errors frequently impact meaning.  Vocabulary is very simple and limited.  A few words are spelled correctly, and basic punctuation is occasionally accurate.
* **Minimal (1 Mark):** Multiple errors in sentence structures, spelling, and word usage significantly impede understanding.
* **Nonexistent (0 Marks):** Not enough language present to assess.""",
        "organization": """Grade the organization of the above student writing based on the following marking scheme, justify your markings.
**Organization (O)**

* **Excellent (7-6 Marks):** Text is highly organized and effectively structured with a clear and logical progression of ideas.  Cohesion is seamless and sophisticated, using a variety of cohesive devices. Overall structure is coherent, sophisticated, and perfectly suited to the genre and text type.
* **Good (5 Marks):** Text is well-organized with a logical development of ideas.  Cohesion is clear and effective, using strong cohesive ties.  Overall structure is coherent, sophisticated, and appropriate to the genre and text type.
* **Fair (4 Marks):** Parts of the text have clearly defined topics. Cohesion is present in some parts, but may be inconsistent. Some cohesive ties are used.  Overall structure is mostly coherent and generally appropriate to the genre and text type.
* **Weak (3 Marks):** The text shows some attempt at organization, but the structure may be unclear or illogical. Simple cohesive ties are used inconsistently, and cohesion is often fuzzy. A limited range of cohesive devices is used.
* **Very Weak (2 Marks):** Some attempts are made to organize the text, but the connection between ideas is often weak. Cohesive devices are used sparingly and may be ineffective.
* **Minimal (1 Mark):** A minimal attempt is made to organize the text, but the structure is largely unclear. Very limited use of cohesive devices.
* **Nonexistent (0 Marks):** Text lacks any discernible organization.  Words, phrases, or sentences are disconnected. Cohesive devices are almost entirely absent.
""",
        "content": """Grade the content of the above student writing based on the following marking scheme, justify your markings.
**Content (C)**

* **Excellent (7-6 Marks):** Fully addresses the question with complete relevance. Ideas are well-developed, supported, and demonstrate creativity and imagination where appropriate. Shows a strong awareness of the audience.
* **Good (5 Marks):** Adequately addresses the question with mostly relevant content. Some ideas are well-developed and supported, showing creativity and imagination at times. Demonstrates some awareness of the audience.
* **Fair (4 Marks):** Just satisfies the requirements with some relevant ideas, but may contain gaps or redundant information.  Development of ideas is limited, and creativity and imagination may be present but inconsistently. Shows occasional awareness of the audience.
* **Weak (3 Marks):** Partially addresses the question with some relevant ideas, but significant gaps exist in understanding. Ideas are not well-developed, and there may be repetition.  Struggles to orient the reader effectively to the topic.
* **Very Weak (2 Marks):** Shows very limited attempts to fulfill the requirements. Content is intermittently relevant with few developed ideas. May include misconceptions or inaccurate information. Very limited awareness of audience.
* **Minimal (1 Mark):** Inadequate content heavily reliant on prompts. Few ideas are present, and none are developed.  Content may be copied from prompts or reading texts. Almost total lack of awareness of audience.
* **Nonexistent (0 Marks):** Totally inadequate, irrelevant, or memorized content copied directly from prompts or reading texts. No awareness of audience.
"""
    }

    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="token-abc123",
        )

    def send_msg(self, message, system):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message

    def get_chat_response(self, chats: List[Chat], name: str, background: str, writing_prompt: str) -> str:
        chat_hist = ""
        for chat in chats:
            chat_hist += f"\n{str(chat)}"

        return self.send_msg(
            self.chat_response_prompt.format(
                chat_hist=chat_hist,
                name=name,
                background=background,
                writing_prompt=writing_prompt), 
            self.chat_response_sys)

    def summarize_chat(self, chats: List[Chat]) -> str:
        chat_hist = ""
        for chat in chats:
            chat_hist += f"\n{str(chat)}"

        return self.send_msg(
            self.summarize_chat_prompt(chat_hist=chat_hist), 
            self.summarize_chat_sys)


    def generate_pals(self, essay_prompt: str) -> str:
        return self.send_msg(
            self.generate_pal_prompt.format(essay_prompt=essay_prompt), 
            self.generate_pal_sys
        )

    def get_writing_suggestion(
            self,
            writing: str,
            grading_aspect: Literal["language", "organization", "content"],
            ) -> str:

        return self.send_msg(
            self.chat_response_prompt.format(
                writing=writing,
                writing_suggestion_prompt=self.writing_rubrics[grading_aspect]
            ),
            self.writing_suggestion_sys)
