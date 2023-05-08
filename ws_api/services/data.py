from flask import request

from ..repositories import data

def find_data():
  all_data = data.find()
  return all_data

def create_data():
  data_ = request.get_json()
  post_data = data.insert(data_)
  print(post_data)
  return "OK"