import sqlite3

from popoll_backend.model.db.option import Option
from popoll_backend.query.poll import PollQuery


class GetPoll(PollQuery):
    
    def __init__(self, poll: str):
        super().__init__(poll)

    def process(self, cursor: sqlite3.Cursor) -> None:
        pass
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Option:
        return Option(cursor.execute('SELECT * FROM options').fetchone())