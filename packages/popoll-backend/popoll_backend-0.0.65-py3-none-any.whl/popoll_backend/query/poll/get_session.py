import sqlite3

from popoll_backend.model.db.session import Session
from popoll_backend.query.poll import PollQuery
from popoll_backend.query import fetchlast


class GetSession(PollQuery):
    
    id: int
    session: Session
    
    def __init__(self, poll: str, id: str):
        super().__init__(poll)
        self.id = id

    def process(self, cursor: sqlite3.Cursor) -> None:
        pass

    def buildResponse(self, cursor: sqlite3.Cursor) -> Session:
        return fetchlast(cursor.execute('SELECT * FROM sessions WHERE session_id=?', (self.id,)), Session)