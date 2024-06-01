import glob
import sqlite3
from typing import List
from popoll_backend.model import Payload
from popoll_backend.query import _Query


class Query(_Query):
    
    def run(self) -> Payload:
        answers: List[Payload] = []
        for db in sorted(glob.glob('*.db')):
            # We do not want to break in case a db is incorrect
            try:
                with sqlite3.connect(db) as connection:
                    cursor: sqlite3.Cursor = connection.cursor()
                    self.process(db[0:-3], cursor)
                    answers.append(self.buildResponse(db[0:-3], cursor))
            except Exception as e:
                print(e)
        return self.mergeResponses(answers)
    
    def process(self, db: str, cursor: sqlite3.Cursor) -> None:
        raise NotImplementedError()
    
    def buildResponse(self, db: str, cursor: sqlite3.Cursor) -> Payload:
        raise NotImplementedError()
    
    def mergeResponses(self, answers: List[Payload]) -> Payload:
        raise NotImplementedError()