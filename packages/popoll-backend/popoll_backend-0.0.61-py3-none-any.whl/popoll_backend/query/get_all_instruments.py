import sqlite3
from typing import List

from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.payload.instruments import Instruments
from popoll_backend.query import PollQuery, fetchall


class GetAllInstruments(PollQuery):
    
    instruments: List[Instrument]
    
    def __init__(self, poll: str):
        super().__init__(poll)

    def process(self, cursor: sqlite3.Cursor) -> None:
        pass
            
    def buildResponse(self, cursor: sqlite3.Cursor) -> Instruments:
        return Instruments(fetchall(cursor.execute('SELECT * FROM instruments ORDER BY rank'), Instrument))