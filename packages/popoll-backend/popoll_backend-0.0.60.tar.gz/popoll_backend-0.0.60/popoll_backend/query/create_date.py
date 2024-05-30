import datetime
import sqlite3
from typing import Optional

from popoll_backend.model.db.date import Date
from popoll_backend.query import PollQuery, fetchlast


class CreateDate(PollQuery):
    
    title: str
    date: datetime.date
    time: Optional[datetime.time]
    end_time: Optional[datetime.time]
    
    id: int
    
    def __init__(self, poll: str, title: str, date: datetime.date, time: Optional[datetime.time], end_time: Optional[datetime.time]):
        super().__init__(poll)
        self.title = title
        self.date = date
        self.time = time
        self.end_time = end_time
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        self.id = cursor.execute('INSERT INTO dates(title, date, time, end_time) VALUES (?, ?, ?, ?)', (self.title, self.date, self.time, self.end_time)).lastrowid
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Date:
        return fetchlast(cursor.execute('SELECT * FROM dates WHERE id=?', (self.id,)), Date)