import flask
import sqlite3

from typing import List

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

class _Query():
    
    def run(self) -> Payload:
        raise NotImplementedError()


    
