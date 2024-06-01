#! /usr/bin/python3
import argparse
import sys
import flask
import json
import logging
import logging.handlers
import os

from flask_cors import CORS
from flask_restful import Api, Resource
from functools import wraps
from typing import Any, Dict

from popoll_backend.model.payload.history import History
from popoll_backend.query.all.upload_polls import UploadPolls
from popoll_backend.query.poll.create_answer import CreateAnswer
from popoll_backend.query.poll.create_date import CreateDate
from popoll_backend.query.poll.create_poll import CreatePoll
from popoll_backend.query.poll.create_user import CreateUser
from popoll_backend.query.poll.delete_answer import DeleteAnswer
from popoll_backend.query.poll.delete_date import DeleteDate
from popoll_backend.query.all.delete_old_dates import DeleteOldDates
from popoll_backend.query.poll.delete_user import DeleteUser
from popoll_backend.query.poll.get_all_instruments import GetAllInstruments
from popoll_backend.query.all.get_all_sessions import GetAllSession
from popoll_backend.query.poll.get_answer import GetAnswer
from popoll_backend.query.poll.get_date import GetDate
from popoll_backend.query.poll.get_date_details import GetDateDetails
from popoll_backend.query.poll.get_dates import GetDates
from popoll_backend.query.poll.get_instruments import GetInstruments
from popoll_backend.query.poll.get_poll import GetPoll
from popoll_backend.query.poll.get_search_answer import GetSearchAnswer
from popoll_backend.query.poll.get_session import GetSession
from popoll_backend.query.poll.get_user_details import GetUserDetails
from popoll_backend.query.poll.get_user_with_instruments import GetUserWithInstruments
from popoll_backend.query.poll.get_users import GetUsers
from popoll_backend.query.poll.update_answer import UpdateAnswer
from popoll_backend.query.poll.update_date import UpdateDate
from popoll_backend.query.poll.update_poll import UpdatePoll
from popoll_backend.query.poll.create_session import CreateSession
from popoll_backend.query.poll.update_user import UpdateUser


app = flask.Flask(__name__)
CORS(app)
api = Api(app)


def body(request: flask.request, param: str, default: Any=None, mandatory=True):
    if request.data != None:
        _body = json.loads(request.data)
        return _body[param] if mandatory else _body.get(param, default)
    else:
        return flask.abort(400, f'Missing parameter [{param}]') if mandatory else default

def queryParam(request: flask.request, param: str) -> bool:
    return request.args.get(param, '') == 'true'

def history(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        _poll = kwargs.get('poll')
        res = f(*args, **kwargs)
        os.makedirs(os.path.join('.history', _poll), exist_ok=True)
        logger = logging.getLogger('my_logger')
        logger.handlers.clear()
        handler = logging.handlers.RotatingFileHandler(os.path.join('.history', _poll, f'{_poll}.history.log'), maxBytes=1024*1024, backupCount=10)
        logger.addHandler(handler)
        logger.warning(json.dumps(History(flask.request, res, kwargs).toJSON()))
        return res
    return decorated





class PollPollEndpoint(Resource):
    def get(self, poll: str) -> str: return GetPoll(poll).run().toJSON()
    
    @history
    def post(self, poll:str) -> str: return CreatePoll(poll, body(flask.request, 'name', mandatory=False, default=poll), body(flask.request, 'instruments', mandatory=False, default=[]), body(flask.request, 'color', mandatory=False, default="#000000")).run().toJSON()
    
    @history
    def put(self, poll:str) -> str: return UpdatePoll(poll, body(flask.request, 'name'), body(flask.request, 'color')).run().toJSON()
    
    
    

class PollInstrumentsEndpoint(Resource):
    def get(self, poll: str) -> str: 
        if queryParam(flask.request, 'used_only'):
            return GetInstruments(poll).run().toJSON()
        else:
            return GetAllInstruments(poll).run().toJSON()
    
    






class PollUsersEndpoint(Resource):
    def get(self, poll: str) -> str: return GetUsers(poll).run().toJSON()
    
    @history
    def post(self, poll: str) -> str: return CreateUser(poll, body(flask.request, 'user')['name'], body(flask.request, 'main_instrument')['id'], [i['id'] for i in body(flask.request, 'instruments')]).run().toJSON()



class PollUserEndpoint(Resource):
    def get(self, poll: str, id:int) -> str: 
        if queryParam(flask.request, 'details'):
            return GetUserDetails(poll, id).run().toJSON()
        else:
            return GetUserWithInstruments(poll, id).run().toJSON()
    
    @history
    def put(self, poll: str, id: int) -> str: return UpdateUser(poll, id, body(flask.request, 'user')['name'], body(flask.request, 'main_instrument')['id'], [i['id'] for i in body(flask.request, 'instruments')]).run().toJSON()
    
    @history
    def delete(self, poll: str, id: int) -> str: return DeleteUser(poll, id).run().toJSON()







class PollDatesEndpoint(Resource):
    def get(self, poll: str) -> str: return GetDates(poll).run().toJSON()
    
    @history
    def post(self, poll: str) -> str: return CreateDate(
        poll, 
        body(flask.request, 'title'), 
        body(flask.request, 'date'), 
        body(flask.request, 'time', mandatory=False), 
        body(flask.request, 'end_time', mandatory=False),
        body(flask.request, 'is_frozen'), 
    ).run().toJSON()



class PollDateEndpoint(Resource):
    def get(self, poll: str, id:int) -> str:
        if queryParam(flask.request, 'details'):
            return GetDateDetails(poll, id).run().toJSON()
        else:
            return GetDate(poll, id).run().toJSON()
    
    @history
    def put(self, poll: str, id: int) -> str: return UpdateDate(
        poll, 
        id, 
        body(flask.request, 'title'), 
        body(flask.request, 'date'), 
        body(flask.request, 'time', mandatory=False), 
        body(flask.request, 'end_time', mandatory=False),
        body(flask.request, 'is_frozen')
    ).run().toJSON()
    
    @history
    def delete(self, poll: str, id: int) -> str: return DeleteDate(poll, id).run().toJSON()







class PollAnswersEndpoint(Resource):
    
    @history
    def post(self, poll: str) -> str: return CreateAnswer(poll, body(flask.request, 'user_id'), body(flask.request, 'date_id')).run().toJSON()


class PollAnswerEndpoint(Resource):
    
    def get(self, poll: str, id:int) -> str: return GetAnswer(poll, id).run().toJSON()
    
    @history
    def put(self, poll: str, id: int) -> str: return UpdateAnswer(poll, id, body(flask.request, 'response')).run().toJSON()
    
    @history
    def delete(self, poll: str, id: int) -> str: return DeleteAnswer(poll, id).run().toJSON()

class PollGetAnswerEndpoint(Resource):
    def get(self, poll: str, userId: int, dateId: int) -> str: return GetSearchAnswer(poll, userId, dateId).run().toJSON()


class PollSessionEndpoint(Resource):
    def get(self, poll: str, id: str) -> str: return GetSession(poll, id).run().toJSON()
    
    @history
    def post(self, poll: str, id: str) -> str: return CreateSession(poll, id, body(flask.request, 'user_id')).run().toJSON()




class SessionEndpoint(Resource):
    def get(self, id: str) -> str: return GetAllSession(id).run().toJSON()


class DatesEndpoint(Resource):
    def delete(self) -> str: return DeleteOldDates().run().toJSON()
    
class PollsEndpoint(Resource):
    def post(self) -> str: return UploadPolls().run().toJSON()


api.add_resource(SessionEndpoint, '/session/<string:id>')
api.add_resource(DatesEndpoint, '/date')
api.add_resource(PollsEndpoint, '/poll')

api.add_resource(PollPollEndpoint, '/<string:poll>')
api.add_resource(PollInstrumentsEndpoint, '/<string:poll>/instrument')
api.add_resource(PollUsersEndpoint, '/<string:poll>/user')
api.add_resource(PollUserEndpoint, '/<string:poll>/user/<int:id>')
api.add_resource(PollDatesEndpoint, '/<string:poll>/date')
api.add_resource(PollDateEndpoint, '/<string:poll>/date/<int:id>')
api.add_resource(PollAnswersEndpoint, '/<string:poll>/answer')
api.add_resource(PollAnswerEndpoint, '/<string:poll>/answer/<int:id>')
api.add_resource(PollGetAnswerEndpoint, '/<string:poll>/answer/<int:userId>/<int:dateId>')
api.add_resource(PollSessionEndpoint, '/<string:poll>/session/<string:id>')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='the hostname to listen on', default='0.0.0.0')
    parser.add_argument('--port', help='the port of the webserver', default=4444)
    parser.add_argument('--debug', help='Enable debugging', action='store_true')
    return parser

def run(args):
    app.run(debug=args.debug, host=args.host, port=args.port)

if __name__ == '__main__':
    args = get_options().parse_args()
    run(args)
