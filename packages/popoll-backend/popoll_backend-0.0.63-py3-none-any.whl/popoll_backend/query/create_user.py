import flask
import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from popoll_backend.model.db.user_instruments import UserInstruments
from popoll_backend.model.payload.user_with_instruments import UserWithInstruments
from popoll_backend.query import PollQuery, fetchall, fetchlast


class CreateUser(PollQuery):
    
    name: str
    main_instrument: int
    instruments: List[int]
    
    id: int
    
    def __init__(self, poll: str, name: str, main_instrument: int, instruments: List[int]):
        super().__init__(poll)
        self.name = name
        self.main_instrument = main_instrument
        self.instruments = instruments
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        self.id = cursor.execute('INSERT INTO users(name) VALUES(?)', (self.name,)).lastrowid
        rows = [(self.id, self.main_instrument, True)] + [(self.id, instru, False) for instru in self.instruments if not instru == self.main_instrument]
        cursor.executemany('INSERT INTO user_instruments(user_id, instrument_id, is_main) VALUES(?, ?, ?)', rows)
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return UserWithInstruments(
            user=fetchlast(cursor.execute('SELECT * FROM users WHERE id=?', (self.id,)), User), 
            instruments=fetchall(cursor.execute('SELECT * FROM instruments'), Instrument), 
            user_instruments=fetchall(cursor.execute('SELECT * from user_instruments where user_id=?', (self.id,)), UserInstruments)
        )
    
    def error(self, e: sqlite3.Error):
        if isinstance(e, sqlite3.IntegrityError):
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                flask.abort(409, f'User with name {self.name} already exists.')