from typing import Literal

from pydantic import BaseModel


class ChatSummary(BaseModel):
    summary: str


class Pal(BaseModel):
    name: str
    occupation: str
    description: str
    analysis: str

    def __init__(self, name: str, occupation: str, description: str, analysis: str = ""):
        super().__init__(name=name, occupation=occupation, description=description, analysis=analysis)


class Chat(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

    def __str__(self) -> str:
        return f"{self.role}: {self.content}"