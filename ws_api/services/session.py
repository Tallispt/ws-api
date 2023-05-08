from uuid import uuid4
from flask import request
from bson import ObjectId

from ..utils.decode import check_password_parity
from ..repositories import session, user

def create_session():
  user_data = request.json
  username, password = user_data.values()

  #TODO Validate username and password
  
  existing_user = user.find_by_username(username)

  if(not existing_user):
    existing_user = user.find_by_email(username)
  if(not existing_user):
    raise Exception('Login_error')

  user_id, user_username, user_email, user_password = existing_user.values()

  check = check_password_parity(password, user_password)

  if(not check):
    raise Exception('Login_error')

  # TODO Session rules

  uuid_obj = uuid4()
  # data = {
  #   "user": user_id,
  #   "token": uuid_obj,
  #   "isValid": True
  # }
  # value = session.insert(data)
  # print(value)
  # _, username, token, isValid, _id = data.values()

  # reposponse = {
  #   "id": ObjectId(_id),
  #   "username": username,
  #   "token": str(token),
  #   "isValid": isValid
  # }

  # return reposponse
  return {}

def login():
  d = request.json
  if 'username' not in d or 'password' not in d:
    raise Exception("Unable to authenticate")
  
  return {}