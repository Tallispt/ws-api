from functools import partial
from http import HTTPStatus

from flask import Blueprint

from ..middlewares.authorization import token_required
from ..middlewares.validation import validate_body
from ..schemas.result import ResultBodySchema
from ..services import result

validate = partial(validate_body, schema=ResultBodySchema)

result_bp = Blueprint("result", __name__, url_prefix="/result")


@result_bp.route("", methods=["GET"])
@token_required
def get_results():
    try:
        response = result.find_all_results()
        return response, HTTPStatus.OK

    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@result_bp.route("/<id>", methods=["GET"])
@token_required
def get_result(id):
    try:
        response = result.find_result(id)
        return response, HTTPStatus.OK

    except Exception as e:
        if str(e) == "Not_found_error":
            return {"error": "Result not found!"}, HTTPStatus.NOT_FOUND
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@result_bp.route("", methods=["POST"])
@token_required
@validate
def post_results():
    try:
        response = result.create_result()
        return response, HTTPStatus.OK

    except Exception as e:
        if str(e) == "Inexistent_data_error":
            return {"error": "Item not found."}, HTTPStatus.NOT_FOUND
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@result_bp.route("/<id>", methods=["PUT"])
@token_required
def put_result(id):
    try:
        response = result.update_result(id)
        return response, HTTPStatus.OK

    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@result_bp.route("/<id>", methods=["DELETE"])
@token_required
def delete_result(id):
    try:
        response = result.remove_result(id)
        return response, HTTPStatus.OK

    except Exception as e:
        if str(e) == "'NoneType' object is not subscriptable":
            return {"error": "Result not found!"}, HTTPStatus.NOT_FOUND
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
