import glob
import flask
import os
import sqlite3

from typing import List, Optional

from popoll_backend.model import Payload


def fetchall(cursor: sqlite3.Cursor, ttype: type) -> List[type]:
        return [ttype(row) for row in cursor.fetchall()]

def fetchlast(cursor: sqlite3.Cursor, ttype: type) -> type:
        res = fetchall(cursor, ttype)
        if len(res) > 0:
            return res[-1]
        flask.abort(404, 'Not found')

def is_date_frozen(cursor: sqlite3.Cursor, date_id: int) -> bool:
    res = cursor.execute('SELECT is_frozen FROM dates WHERE id=?', (date_id,)).fetchone()
    if res != None and len(res) > 0:
        return res[0]
    else:
        flask.abort(400, 'Not found')

def get_date_id(cursor:sqlite3.Cursor, answer_id: int) -> int:
    res = cursor.execute('SELECT date_id FROM answers WHERE id=?', (answer_id,)).fetchone()
    if res != None and len(res) > 0:
        return res[0]
    else:
        flask.abort(404, 'Not found')

class Query:
    
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

class PollQuery(Query):
    
    fail_if_db_exists: bool = False
    fail_if_db_not_exists: bool = True
    
    def __init__(self, poll: str):
        self.poll = poll
        self.db_file = f'{poll}.db'
        if self.fail_if_db_exists and os.path.exists(self.db_file):
            flask.abort(409, f'The poll [{poll}] already exists.')
        if self.fail_if_db_not_exists and not os.path.exists(self.db_file):
            flask.abort(400, f'The poll [{poll}] does not exist.')
    
    def run(self, cursor: Optional[sqlite3.Cursor]=None) -> Payload:
        if cursor:
            return self._run(cursor)
        else:
            with sqlite3.connect(self.db_file) as connection:
                _cursor: sqlite3.Cursor = connection.cursor()
                _cursor.execute("PRAGMA foreign_keys = ON")
                # _cursor.execute("ATTACH DATABASE 'instruments.db' AS instruments;")
                return self._run(_cursor)
            
    def _run(self, cursor: sqlite3.Cursor) -> Payload:
        try:
            self.process(cursor)
            return self.buildResponse(cursor)
        except sqlite3.Error as e:
            print(e)
            self.error(e)
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                flask.abort(400, f'ForeignKey error. You refer to a not existing resource')
            if e.sqlite_errorcode == sqlite3.SQLITE_ERROR:
                flask.abort(500, 'Main error. Are you sure database exists?')
            return None
    
    def process(self, cursor: sqlite3.Cursor) -> None:
        raise NotImplementedError()
    
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        raise NotImplementedError()
    
    def error(self, e: sqlite3.Error) -> None:
        pass
    
