
from typing import List
from popoll_backend.model import Payload
from popoll_backend.model.payload.user_with_instruments import UserWithInstruments


class UsersPayloadDetails(Payload):
    
    def __init__(self, users: List[UserWithInstruments]):
        self.users: List[UserWithInstruments] = users