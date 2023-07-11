from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from http import HTTPStatus

health_bp = Blueprint("health", __name__, url_prefix='/health')

@health_bp.route('', methods=['GET'])
def health():
  return {}, HTTPStatus.OK

@health_bp.route('', methods=['POST'])
def error_handler_example():
  try:
    data = request.json
    c = data['a']/data['b']
    return str(c), HTTPStatus.ACCEPTED
  except ZeroDivisionError as error:
    print(BadRequest)
    return {'error_message': str(error)}, HTTPStatus.BAD_REQUEST