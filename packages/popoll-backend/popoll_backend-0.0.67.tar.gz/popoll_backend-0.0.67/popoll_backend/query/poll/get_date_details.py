import sqlite3

from popoll_backend.model.db.answer import Answer
from popoll_backend.model.db.date import Date
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.date_details import DateDetails
from popoll_backend.query.poll import PollQuery
from popoll_backend.query import fetchall, fetchlast


class GetDateDetails(PollQuery):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id

    def process(self, cursor: sqlite3.Cursor) -> None:
        pass

    def buildResponse(self, cursor: sqlite3.Cursor) -> DateDetails:
        globally_used_instruments = [row[0] for row in cursor.execute('SELECT DISTINCT instrument_id FROM user_instruments').fetchall()]
        return DateDetails(
            date=fetchlast(cursor.execute('SELECT * FROM dates where id=?', (self.id,)), Date), 
            answers=fetchall(cursor.execute('SELECT * FROM answers where date_id=?', (self.id,)), Answer),
            users=fetchall(cursor.execute('SELECT * FROM users ORDER BY name COLLATE NOCASE'), User),     
            instruments=[instr for instr in fetchall(cursor.execute('SELECT * FROM instruments ORDER BY rank'), Instrument) if instr.id in globally_used_instruments],
            user_instruments=fetchall(cursor.execute('SELECT * FROM user_instruments'), UserInstruments)
        )