import bcrypt
from uuid import uuid4
from http import HTTPStatus
from flask import Blueprint, request

from ..utils.decode_utils import parse_bytes
from ..repositories import user_repository, session_repository

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('', methods=['POST'])
def create_session():
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