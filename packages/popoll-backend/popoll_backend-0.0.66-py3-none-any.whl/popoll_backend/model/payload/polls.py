from typing import List, Optional
from popoll_backend.model import Payload


class Poll(Payload):
    
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

class Polls(Payload):
    
    def __init__(self, polls: List[Poll]):
        self.polls: List[Poll] = polls
