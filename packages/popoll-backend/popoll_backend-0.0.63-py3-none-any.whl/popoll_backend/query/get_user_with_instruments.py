import sqlite3

from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.user_with_instruments import UserWithInstruments
from popoll_backend.query import PollQuery, fetchall, fetchlast


class GetUserWithInstruments(PollQuery):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        pass
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> UserWithInstruments:
        return UserWithInstruments(
            user=fetchlast(cursor.execute('SELECT * FROM users WHERE id=?', (self.id,)), User), 
            instruments=fetchall(cursor.execute('SELECT * FROM instruments ORDER BY rank'), Instrument),
            user_instruments=fetchall(cursor.execute('SELECT * FROM user_instruments WHERE user_id=?', (self.id,)), UserInstruments)
        )
        
        
        