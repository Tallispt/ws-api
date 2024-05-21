from functools import wraps
from http import HTTPStatus

from flask import request
from marshmallow import ValidationError


def validate_body(func, schema):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            data = request.json
            result = schema().load(data)
            for item in result:
                if result[item] == "":
                    raise ValidationError("Not allowed blanck value ['" + item + "']")
            return func(*args, **kwargs)
        except ValidationError as e:
            return {"error": str(e.messages)}, HTTPStatus.FORBIDDEN

    return decorated


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            data = request.files
            if "file" not in data:
                raise ValidationError("No 'file' found.")

            file = data["file"]
            if file.filename == "":
                raise ValidationError("No selected file.")

            if not file or not allowed_file(file.filename):
                raise ValidationError("File not supported.")
            return func(*args, **kwargs)
        except ValidationError as e:
            return {"error": str(e.messages)}, HTTPStatus.FORBIDDEN

    return decorated


def validate_form(func, schema):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            form = request.form
            result = schema().load(form)
            for item in result:
                if result[item] == "":
                    raise ValidationError("Not allowed blanck value ['" + item + "']")

            return func(*args, **kwargs)
        except ValidationError as e:
            return {"error": str(e.messages)}, HTTPStatus.FORBIDDEN

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
