import sqlite3
from typing import List

from popoll_backend.model import Payload
from popoll_backend.model.payload.empty import Empty
from popoll_backend.model.payload.polls import Poll, Polls
from popoll_backend.query import Query


class GetAllSession(Query):
    
    id: int
    
    def __init__(self, id: str):
        self.id = id
        
    def process(self, db: str, cursor: sqlite3.Cursor) -> None:
        pass
        
    def buildResponse(self, db: str, cursor: sqlite3.Cursor) -> Poll | Empty:
        if cursor.execute('SELECT COUNT(*) FROM sessions WHERE session_id=?', (self.id,)).fetchone()[0] > 0:
            return Poll(db, cursor.execute('SELECT name FROM options').fetchone()[0])
        else:
            return Empty()
        
    def mergeResponses(self, answers: List[Payload]) -> Payload:
        return Polls(polls=[a for a in answers if not a.isEmpty])
    
    