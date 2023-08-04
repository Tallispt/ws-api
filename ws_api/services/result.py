from flask import request
from bson import json_util

from ..repositories import result
from ..utils import cammel_snake

def find():
  result_data = result.find_all()

  if(not result_data):
    return []

  list_cur = list(result_data)
  response = json_util.dumps(list_cur)
  return response