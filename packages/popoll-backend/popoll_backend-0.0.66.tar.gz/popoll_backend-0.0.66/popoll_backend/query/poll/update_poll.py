import sqlite3

from popoll_backend.model.db.option import Option
from popoll_backend.query.poll import PollQuery


class UpdatePoll(PollQuery):
    
    name: str
    color: str
    
    def __init__(self, poll: str, name: str, color: str):
        super().__init__(poll)
        self.name = name
        self.color = color
        
    def process(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('UPDATE options SET name=?, color=?', (self.name, self.color))
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Option:
        return Option(cursor.execute('SELECT * FROM options').fetchone())