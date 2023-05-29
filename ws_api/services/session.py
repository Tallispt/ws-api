from uuid import uuid4
from marshmallow import ValidationError

from ..utils.decode import check_password_parity
from ..repositories import session, user
from ..schemas.user import SignInSchema
from ..middlewares.validation import validation

def create_session():
  body = validation(SignInSchema)
  username = body['username']
  password = body['password']

  if(username == "" or password == ""):
    raise ValidationError("Not allowed blanck values")

  db_user = user.find_by_username(username)

  if(not db_user):
    db_user = user.find_by_email(username)
  if(not db_user):
    raise Exception('Login_error')
  
  user_id, user_username, user_email, user_password = db_user.values()

  check = check_password_parity(password, user_password)

  if(not check):
    raise Exception('Login_error')

  uuid_obj = str(uuid4())
  session.insert(user_id, uuid_obj)

  return {'user': user_username, 'token': uuid_obj}

def delete():
  return session.delete_all()