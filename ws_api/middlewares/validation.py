from flask import request
from functools import wraps
from http import HTTPStatus
from marshmallow import ValidationError

def validate_body(func, schema):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            data = request.json
            result = schema().load(data)
            for item in result:
                if(result[item] == ""):
                    raise ValidationError("Not allowed blanck value ['" + item + "']")
            return func(*args, **kwargs)
        except ValidationError as e:
            return {'error': str(e.messages)}, HTTPStatus.FORBIDDEN
        
    return decorated

# def validate_query(func, query, schema):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         try:
#             query = request.args.get(query)
#             result = schema().load(data)
#             for item in result:
#                 if(result[item] == ""):
#                     raise ValidationError("Not allowed blanck value ['" + item + "']")
#             return func(*args, **kwargs)
#         except ValidationError as e:
#             return {'error': str(e.messages)}, HTTPStatus.FORBIDDEN
        
#     return decorated