from uuid import uuid4
from flask import request

from ..utils.decode import check_password_parity, parse_json
from ..repositories import session, user

def create_session():
  user_data = request.json

  #TODO Validate username and password
  
  if 'username' not in user_data or 'password' not in user_data:
    raise Exception("Unable to authenticate")
  
  username, password = user_data.values()

  existing_user = user.find_by_username(username)

  if(not existing_user):
    existing_user = user.find_by_email(username)
  if(not existing_user):
    raise Exception('Login_error')
  
  user_id, user_username, user_email, user_password = existing_user.values()

  # TODO Session rules

  check = check_password_parity(password, user_password)

  if(not check):
    raise Exception('Login_error')

  uuid_obj = str(uuid4())
  session.insert(user_id, uuid_obj)

  return {'user': user_username, 'token': uuid_obj}

def login():
  user_data = request.json
  return {}

def delete():
  return session.delete_all()