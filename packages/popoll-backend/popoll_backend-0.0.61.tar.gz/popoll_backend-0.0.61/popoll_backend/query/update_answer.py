import sqlite3
from typing import Optional

import flask

from popoll_backend.model import Payload
from popoll_backend.model.db.answer import Answer
from popoll_backend.query import PollQuery, fetchlast, get_date_id, is_date_frozen
from popoll_backend.query.get_answer import GetAnswer


class UpdateAnswer(PollQuery):
    
    id: int
    response: Optional[bool]
    
    def __init__(self, poll:str, id: int, response: Optional[bool]):
        super().__init__(poll)
        self.id = id
        self.response = response
    
    def process(self, cursor: sqlite3.Cursor):
        if is_date_frozen(cursor, get_date_id(cursor, self.id)):
            flask.abort(403, 'Date is frozen. Cannot modify')
        cursor.execute('UPDATE answers SET response=? WHERE id=?', (self.response, self.id))
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return fetchlast(cursor.execute('SELECT * FROM answers WHERE id=?', (self.id,)), Answer)