import sqlite3

import flask

from popoll_backend.model.db.answer import Answer
from popoll_backend.query import PollQuery, fetchlast, is_date_frozen


class CreateAnswer(PollQuery):
    
    user_id: int
    date_id: int
    
    id: int
    
    def __init__(self, poll:str, user_id: int, date_id: int):
        super().__init__(poll)
        self.user_id = user_id
        self.date_id = date_id
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        if is_date_frozen(cursor, self.date_id):
            flask.abort(403, 'Date is frozen. Cannot modify')
        self.id = cursor.execute('INSERT INTO answers(user_id, date_id, response) VALUES (?, ?, ?)', (self.user_id, self.date_id, True)).lastrowid
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Answer:
        return fetchlast(cursor.execute('SELECT * FROM answers WHERE id=?', (self.id,)), Answer)
    
    def error(self, e: sqlite3.Error):
        if isinstance(e, sqlite3.IntegrityError):
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                flask.abort(409, f'Answer for this user already exists. PUT should be triggered instead.')
