from flask import request

from ..repositories import data
from ..middlewares.validation import validation
from ..schemas.data import DataBodySchema
from ..repositories import data

def find_data():
  response = data.find()
  return response

def create_data():
  body = validation(DataBodySchema)

  name = body['name']
  file = body['file']

  data.insert(name, file)

  return {}