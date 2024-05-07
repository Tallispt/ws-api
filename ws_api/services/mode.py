from flask import request
from bson import json_util

from ..repositories import mode
from ..utils import cammel_snake

def find_user_modes():
  user_id = request.environ['user_id']

  mode_data = mode.find_all(user_id)

  if(not mode_data):
    return []

  list_cur = list(mode_data)
  response = json_util.dumps(list_cur)
  return response

def find_mode(id):
  user_id = request.environ['user_id']

  mode_data = mode.find_by_id(user_id, id)
  if(not mode_data):
    return []

  response = json_util.dumps(mode_data)
  return response

def create_mode():
  user_id = request.environ['user_id']

  body = request.json
  _body = cammel_snake.convert_json(body)

  title_exists = mode.find_by_title(_body["title"], user_id)

  if(title_exists):
    raise Exception("Conflict_error")

  new_mode = mode.insert(_body, user_id)

  return {"modeId": str(new_mode.inserted_id)}

def update_mode(id):
  user_id = request.environ['user_id']

  body = request.json

  data = cammel_snake.convert_json(body)
  print(data)

  updated_mode = mode.update(user_id, id, data)
  return {"modeId": str(updated_mode["_id"])}


def remove_mode(id):
  user_id = request.environ['user_id']

  deleted_mode = mode.delete(user_id, id)

  return {"modeId": str(deleted_mode["_id"])}