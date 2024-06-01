from __future__ import annotations
import datetime
import sqlite3
from typing import Any, List, Optional

from popoll_backend.model import Payload


class Date(Payload):
    
    def __init__(self, data: List[Any]):
        self.id: int = data[0]
        self.title: str = data[1]
        self.date: datetime.date = datetime.date.fromisoformat(data[2])
        self.time: Optional[datetime.time] = datetime.time.fromisoformat(data[3]) if data[3] else None
        self.end_time: Optional[datetime.time] = datetime.time.fromisoformat(data[4]) if data[4] else None
        self.is_frozen: bool = bool(data[5])
        self.is_old: bool = self.isOlder()
        
    @classmethod
    def create_table(cls):
        return """ CREATE TABLE IF NOT EXISTS dates (
            id integer PRIMARY KEY AUTOINCREMENT,
            title text NOT NULL,
            date text NOT NULL,
            time text,
            end_time text,
            is_frozen boolean NOT NULL
        ); """
        
    def isOlder(self, compare: datetime.date=datetime.date.today()):
        return self.date < compare
