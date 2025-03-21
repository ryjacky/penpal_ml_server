from dataclasses import dataclass

@dataclass
class JourneyMessage:
    journey_id: int
    content: str
    is_from_user: bool
    user_id: str