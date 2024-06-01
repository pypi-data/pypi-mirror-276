import sqlite3
from typing import List

from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.users import Users
from popoll_backend.query.poll import PollQuery
from popoll_backend.query import fetchall


class GetUsers(PollQuery):
    
    def __init__(self, poll: str):
        super().__init__(poll)
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        pass

    def buildResponse(self, cursor: sqlite3.Cursor) -> Users:
        return Users(fetchall(cursor.execute('SELECT * FROM users ORDER BY name COLLATE NOCASE'), User))