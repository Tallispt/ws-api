from flask import Blueprint, request
import bcrypt
from ws_api.utils.decode_utils import parse_bytes
from ws_api.repositories import user_repository, session_repository
from uuid import uuid4
from http import HTTPStatus

user_bp = Blueprint("users", __name__, url_prefix="")
# TODO architecture (Routes, Controllers and Services) - Repositories DONE

@user_bp.route('/sign-up', methods=['POST'])
def create_user():
  user_data = request.get_json()
  username, email, password = user_data.values()
  
  # TODO Validate username and password
  # https://stackoverflow.com/questions/61644396/flask-how-to-make-validation-on-request-json-and-json-schema

  # TODO try error
  
  existing_user = user_repository.find_by_username(username)
  existing_email = user_repository.find_by_email(email)
  if(existing_user or existing_email):
    return {"message": "User already exists"}, HTTPStatus.CONFLICT

  hash = bcrypt.hashpw(parse_bytes(password), bcrypt.gensalt())

  user_repository.insert(username, email, hash.decode('utf-8'))

  response = {"username": username}
  return response, HTTPStatus.CREATED

@user_bp.route('/sign-in', methods=['POST'])
def get_all_user():
  user_data = request.get_json()
  username, password = user_data.values()

  #TODO Validate username and password
  
  user = user_repository.find_by_username(username)
  print(user)

  if(not user):
    user = user_repository.find_by_email(username)

  if(not user):
    return {}, HTTPStatus.BAD_REQUEST
  
  user_id, user_username, user_email, user_password = user.values()

  check = bcrypt.checkpw(parse_bytes(password), parse_bytes(user_password))

  if(not check):
    return {}, HTTPStatus.BAD_REQUEST

  # TODO Session rules

  uuid_obj = uuid4()
  data = {
    "user": user_id,
    "username": user_username,
    "token": uuid_obj,
    "isValid": True
  }
  session_repository.insert(data)

  user, username, token, isValid, _id = data.values()

  reposponse = {
    "id": str(_id),
    "username": username,
    "token": str(token),
    "isValid": isValid
  }

  return reposponse, HTTPStatus.CREATED