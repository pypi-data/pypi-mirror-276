import datetime
import sqlite3
from typing import List, Tuple

from popoll_backend.model import Payload
from popoll_backend.model.db.date import Date
from popoll_backend.model.payload.empty import Empty
from popoll_backend.query import Query, fetchall

def dateBefore(day=datetime.date.today(), years: int=0, days: int=0):
    today = day.isoformat()
    beforeYears = today[0:3] + str(int(today[3])-years) + today[4:] # big hack to replace year in string to get rid of bissectil years
    return (datetime.date.fromisoformat(beforeYears) - datetime.timedelta(days=days))

class DeleteOldDates(Query):
    
    past = dateBefore(years=1)
    
    def process(self, db: str, cursor: sqlite3.Cursor) -> None:
        dates: List[Date] = fetchall(cursor.execute('SELECT * FROM dates'), Date)
        old_dates_ids: List[Tuple[int]] = [(date.id,) for date in dates if date.isOlder(self.past)]
        cursor.executemany('DELETE FROM dates WHERE id=?', old_dates_ids)
    
    def buildResponse(self, db: str, cursor: sqlite3.Cursor) -> Payload:
        return Empty()
    
    def mergeResponses(self, answers: List[Payload]) -> Payload:
        return Empty()
