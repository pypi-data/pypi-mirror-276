import sqlite3
from typing import List

from popoll_backend.model.db.answer import Answer
from popoll_backend.model.db.date import Date
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.option import Option
from popoll_backend.model.db.session import Session
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.id_payload import IdPayload
from popoll_backend.query import PollQuery


class CreatePoll(PollQuery):
    
    fail_if_db_exists: bool = True
    fail_if_db_not_exists: bool = False
    
    name: str
    instruments: List[str]
    color: str
    
    def __init__(self, poll:str, name: str, instruments: List[str], color: str):
        super().__init__(poll)
        self.name = name
        self.instruments = instruments
        self.color = color
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(Option.create_table())
        cursor.execute('INSERT INTO options(name, color) values(?, ?)', (self.name, self.color))
        cursor.execute(Date.create_table())
        cursor.execute(Instrument.create_table())
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Tamborim', 1))
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Agogo', 2))
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Chocalho', 3))
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Repinique', 4))
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Caixa', 5))
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Primeira', 6))
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Segunda', 7))
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Terceira', 8))
        cursor.execute('INSERT OR IGNORE INTO instruments(name, rank) VALUES(?, ?);', ('Timbal', 9))
        cursor.execute(User.create_table())
        cursor.execute(Answer.create_table())
        cursor.execute(UserInstruments.create_table())
        cursor.execute(Session.create_table())
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> IdPayload:
        return IdPayload(0)