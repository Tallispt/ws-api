import bcrypt
from uuid import uuid4
from http import HTTPStatus
from flask import Blueprint, request

from ..utils.decode_utils import parse_bytes
from ..repositories import user_repository

user_bp = Blueprint("users", __name__, url_prefix="/user")

@user_bp.route('', methods=['POST'])
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