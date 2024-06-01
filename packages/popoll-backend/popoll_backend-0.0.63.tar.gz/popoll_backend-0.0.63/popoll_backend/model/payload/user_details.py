from typing import List, Optional
from popoll_backend.model.db.answer import Answer
from popoll_backend.model.db.date import Date
from popoll_backend.model import Payload
from popoll_backend.model.payload.user_with_instruments import UserWithInstruments

class UserDetailsDate():
    
    def __init__(self, user: UserWithInstruments, date: Date, answers: List[Answer]):
        self.date: Date = date
        _ans = [a for a in answers if a.user_id == user.id and a.date_id == date.id]
        self.answer: Optional[Answer] = _ans[0] if len(_ans) > 0 else None
        

class UserDetails(Payload):
    
    def __init__(self, user: UserWithInstruments, answers: List[Answer], dates: List[Date]):
        self.user: UserWithInstruments = user
        self.dates: List[UserDetailsDate] = [UserDetailsDate(user, date, answers) for date in dates]