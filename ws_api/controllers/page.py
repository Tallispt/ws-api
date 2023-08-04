from flask import Blueprint
from http import HTTPStatus
from functools import partial

from ..services.page import find_pages
from ..middlewares.authorization import token_required

page_bp = Blueprint("page", __name__, url_prefix="/page")

@page_bp.route('', methods=['GET'])
@token_required
def get_pages():
  try:
    response = find_pages()
    return response, HTTPStatus.OK
    
  except Exception as e:
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST