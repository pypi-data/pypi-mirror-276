import datetime
import sqlite3

from popoll_backend.model.db.session import Session
from popoll_backend.query.poll import PollQuery
from popoll_backend.query import fetchlast


class CreateSession(PollQuery):
    
    id: int
    
    def __init__(self, poll: str, id: str, user_id: int):
        super().__init__(poll)
        self.id = id
        self.user_id = user_id

    def process(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('DELETE FROM sessions WHERE session_id=?', (self.id,))
        cursor.execute('INSERT INTO sessions(session_id, user_id, datetime) VALUES(?, ?, ?)', (self.id, self.user_id, self.getNow())).lastrowid

    def buildResponse(self, cursor: sqlite3.Cursor) -> Session:
        return fetchlast(cursor.execute('SELECT * FROM sessions WHERE session_id=?', (self.id,)), Session)
    
    def getNow(self) -> str:
        return datetime.datetime.now().isoformat(sep='T', timespec='auto')