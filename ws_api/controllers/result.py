from flask import Blueprint
from http import HTTPStatus

from ..services import result
from ..middlewares.authorization import token_required

result_bp = Blueprint("result", __name__, url_prefix="/result")

@result_bp.route('', methods=['GET'])
@token_required
def get_results():
  try:
    response = result.find()
    return response, HTTPStatus.OK
    
  except Exception as e:
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST