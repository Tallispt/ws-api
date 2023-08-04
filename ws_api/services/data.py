from flask import request
from bson import json_util

from ..utils import base64, image
from ..repositories import data
# import cv2

def generate(data):
  n = 158415
  data_chunks = [data[i:i+n] for i in range(0, len(data), n)]
  for split_data in data_chunks:
      yield split_data

def detect_sensor():
  body = request.json

  file = body['file']
  img = base64.readb64(file)


  new_img = image.detect_contours(img)

  new_file = base64.encode64(new_img)

  return generate(new_file)

def find_data(id):
  if(not id):
    raise Exception()
  
  user_data = data.find_by_id(id)

  if(not user_data):
    raise Exception()
  
  list_cur = list(user_data)
  response = json_util.dumps(list_cur)
  return response

def find_user_data():
  user_id = request.environ['user_id']
  
  user_data = data.find_by_id(user_id)
  
  if(not user_data):
    return []
  
  list_cur = list(user_data)
  response = json_util.dumps(list_cur)
  return response

def create_data():
  user_id = request.environ['user_id']

  body = request.json
  file = body['file']

  # processar os dados e inserir no banco

  new_data = data.insert(user_id, file)

  return {"id": str(new_data.inserted_id)}

def update_data(id):
  user_id = request.environ['user_id']

  body = request.json
  file = body['file']

  data.update(id, user_id, file)

  return {}

def remove_data(id):
  user_id = request.environ['user_id']

  data.delete(id, user_id)

  return {}