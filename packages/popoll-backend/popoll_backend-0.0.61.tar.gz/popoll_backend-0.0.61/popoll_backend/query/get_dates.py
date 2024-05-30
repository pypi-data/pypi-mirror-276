import sqlite3
from typing import List

from popoll_backend.model.db.date import Date
from popoll_backend.model.payload.dates import Dates
from popoll_backend.query import PollQuery, fetchall


class GetDates(PollQuery):
    
    dates: List[Date]
    
    def __init__(self, poll: str):
        super().__init__(poll)

    def process(self, cursor: sqlite3.Cursor):
        pass
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Dates:
        return Dates(fetchall(cursor.execute('SELECT * FROM dates ORDER BY date, time'), Date))