from flask import Blueprint, request
from http import HTTPStatus
from ..repositories import user_repository

from ..database import mongo

session_bp = Blueprint('session', __name__)

@session_bp.route('/', methods=['POST'])
def index():
    return {}, 201