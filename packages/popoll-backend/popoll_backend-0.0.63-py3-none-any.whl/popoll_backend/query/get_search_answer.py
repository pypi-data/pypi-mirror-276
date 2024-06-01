import sqlite3

import flask

from popoll_backend.model.db.answer import Answer
from popoll_backend.query import PollQuery, fetchlast


class GetSearchAnswer(PollQuery):
    
    userId: int
    dateId: int
    
    def __init__(self, poll: str, userId: int, dateId: int):
        super().__init__(poll)
        self.userId = userId
        self.dateId = dateId

    def process(self, cursor: sqlite3.Cursor) -> None:
        pass
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Answer:
        return fetchlast(cursor.execute('SELECT * FROM answers WHERE user_id=? AND date_id=?', (self.userId, self.dateId)), Answer)