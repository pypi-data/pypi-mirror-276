import sqlite3
from popoll_backend.model import Payload
from popoll_backend.model.payload.empty import Empty
from popoll_backend.model.payload.id_payload import IdPayload
from popoll_backend.query import PollQuery


class DeleteDate(PollQuery):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('DELETE FROM dates WHERE id=?', (self.id,))
    
    def buildResponse(self, _: sqlite3.Cursor) -> IdPayload:
        return Empty()
    