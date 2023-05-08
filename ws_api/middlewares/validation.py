from flask import request
from functools import wraps
from http import HTTPStatus
from marshmallow import ValidationError

# def validation(schema):
#     def inner_decorator(f):
#         def wrapped(*args, **kwargs):
#           try:
#               data = request.json
#               result = schema().load(data)
              
#           except ValidationError as e:
#             return {'error': str(e)}, HTTPStatus.FORBIDDEN
        
#           return result

#         return wrapped
#     return inner_decorator

def validation(schema):
    try:
        data = request.json
        result =  schema().load(data)
    
    except ValidationError as e:
      raise ValidationError(e.messages)
    
    return result