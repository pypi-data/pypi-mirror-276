import sqlite3

from popoll_backend.model.db.answer import Answer
from popoll_backend.query.poll import PollQuery
from popoll_backend.query import fetchlast


class GetAnswer(PollQuery):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id

    def process(self, cursor: sqlite3.Cursor) -> None:
        pass
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Answer:
        return fetchlast(cursor.execute('SELECT * FROM answers WHERE id=?', (self.id,)), Answer)