import sqlite3

from popoll_backend.model import Payload
from popoll_backend.model.db.date import Date
from popoll_backend.query.poll import PollQuery
from popoll_backend.query import fetchlast


class GetDate(PollQuery):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id

    def process(self, cursor: sqlite3.Cursor) -> None:
        pass

    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return fetchlast(cursor.execute('SELECT * FROM dates WHERE id=? ORDER BY date, time', (self.id,)), Date)