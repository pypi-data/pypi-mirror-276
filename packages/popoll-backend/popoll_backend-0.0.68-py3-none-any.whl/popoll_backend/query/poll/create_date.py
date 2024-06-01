import datetime
import sqlite3
from typing import Optional

from popoll_backend.model.db.date import Date
from popoll_backend.query.poll import PollQuery
from popoll_backend.query import fetchlast


class CreateDate(PollQuery):
    
    title: str
    date: datetime.date
    time: Optional[datetime.time]
    end_time: Optional[datetime.time]
    is_frozen: bool
    
    id: int
    
    def __init__(self, poll: str, title: str, date: datetime.date, time: Optional[datetime.time], end_time: Optional[datetime.time], is_frozen: bool):
        super().__init__(poll)
        self.title = title
        self.date = date
        self.time = time
        self.end_time = end_time
        self.is_frozen = is_frozen
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        self.id = cursor.execute('INSERT INTO dates(title, date, time, end_time, is_frozen) VALUES (?, ?, ?, ?, ?)', (self.title, self.date, self.time, self.end_time, self.is_frozen)).lastrowid
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Date:
        return fetchlast(cursor.execute('SELECT * FROM dates WHERE id=?', (self.id,)), Date)