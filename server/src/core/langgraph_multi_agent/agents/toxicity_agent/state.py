from typing import TypedDict

class ToxicityState(TypedDict):
    message: str
    is_toxic: bool