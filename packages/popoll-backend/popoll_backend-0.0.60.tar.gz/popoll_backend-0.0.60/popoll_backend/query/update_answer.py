import sqlite3
from typing import Optional

from popoll_backend.model import Payload
from popoll_backend.model.db.answer import Answer
from popoll_backend.query import PollQuery, fetchlast
from popoll_backend.query.get_answer import GetAnswer


class UpdateAnswer(PollQuery):
    
    id: int
    response: Optional[bool]
    
    def __init__(self, poll:str, id: int, response: Optional[bool]):
        super().__init__(poll)
        self.id = id
        self.response = response
    
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('UPDATE answers SET response=? WHERE id=?', (self.response, self.id))
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return fetchlast(cursor.execute('SELECT * FROM answers WHERE id=?', (self.id,)), Answer)