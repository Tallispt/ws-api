from flask import request, make_response, jsonify

from ..repositories import data

def find_data():
  data_ = data.find()
  return jsonify({'page' : data_})

def create_data():
  data_ = request.get_json()
  post_data = data.insert(data_)
  print(post_data)
  return "OK"