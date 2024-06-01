import sqlite3

from popoll_backend.model.db.instrument import Instrument
from popoll_backend.query import PollQuery, fetchlast


class GetInstrument(PollQuery):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        pass
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Instrument:
        return fetchlast(cursor.execute('SELECT * FROM instruments WHERE id=?', (self.id,)), Instrument)