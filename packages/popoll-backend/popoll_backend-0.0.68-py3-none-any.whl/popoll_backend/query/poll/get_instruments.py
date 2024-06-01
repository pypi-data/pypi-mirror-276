import sqlite3
from typing import List

from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.payload.instruments import Instruments
from popoll_backend.query.poll import PollQuery
from popoll_backend.query import fetchall


class GetInstruments(PollQuery):
    
    instruments: List[Instrument]
    
    def __init__(self, poll: str):
        super().__init__(poll)

    def process(self, cursor: sqlite3.Cursor) -> None:
        pass
            
    def buildResponse(self, cursor: sqlite3.Cursor) -> Instruments:
        globally_used_instruments = [row[0] for row in cursor.execute('SELECT DISTINCT instrument_id FROM user_instruments').fetchall()]
        return Instruments([instr for instr in fetchall(cursor.execute('SELECT * FROM instruments ORDER BY rank'), Instrument) if instr.id in globally_used_instruments])