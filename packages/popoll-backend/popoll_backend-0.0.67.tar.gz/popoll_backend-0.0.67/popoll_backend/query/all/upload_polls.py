

import sqlite3
import toml
from typing import List

import requests

from popoll_backend.model import Payload
from popoll_backend.model.payload.empty import Empty
from popoll_backend.model.payload.id_payload import IdPayload
from popoll_backend.query.all import Query


class UploadPolls(Query):
  
  status_code: int
  
  def __init__(self):
    with open("popoll_backend.toml", "rb") as f:
      config = toml.loads(f)
    self.drive_id = config['kdrive']['drive_id']
    self.token = config['kdrive']['token']
    self.folder_id = self.get_folder_id(config['kdrive']['folder'], self.drive_id, self.token)

  def process(self, db: str, cursor: sqlite3.Cursor) -> None:
    with open(f'{db}.db', mode='rb') as file:
      data = file.read()
        
    res = requests.post(
      url=f'https://api.infomaniak.com/3/drive/{self.drive_id}/upload?conflict=version&file_name={db}.db&total_size={len(data)}&directory_id={self.folder_id}', 
      data=data, 
      headers=self.headers(self.token, 'application/octet-stream')
    )
    print(f'[{res.status_code}] {res.json()}')
    self.status_code = res.status_code
      
  def buildResponse(self, db: str, cursor: sqlite3.Cursor) -> IdPayload:
      return IdPayload(self.status_code)
      
  def mergeResponses(self, answers: List[IdPayload]) -> IdPayload:
      return IdPayload(max([a.id for a in answers]) if len(answers) > 0 else 500)

  def get_folder_id(self, folder, drive_id, token):
    rs = requests.get(url=f'https://api.infomaniak.com/3/drive/{drive_id}/files/search', headers=self.headers(token, 'application/json'))
    return [data['id'] for data in (rs.json())['data'] if data['name'] == folder][0]
  
  def headers(self, token, contentType):
    return {
    'Authorization': f'Bearer {token}',
    'Content-Type': contentType
    }