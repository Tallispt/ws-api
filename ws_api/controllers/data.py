from functools import partial
from http import HTTPStatus

from flask import Blueprint

from ..middlewares.authorization import token_required
from ..middlewares.validation import validate_body, validate_file, validate_form
from ..schemas.data import DetectFormsBodySchema
from ..services import data

validate_detection_file = partial(validate_file)
validate_detection_form = partial(validate_form, schema=DetectFormsBodySchema)

data_bp = Blueprint("data", __name__, url_prefix="/data")


@data_bp.route("/detect", methods=["GET", "POST"])
@token_required
@validate_detection_file
@validate_detection_form
def detect_data():
    try:
        response = data.detect_sensor()
        return response, HTTPStatus.CREATED

    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@data_bp.route("/detect/<data_id>", methods=["DELETE"])
@token_required
def delete_detect_data(data_id):
    try:
        response = data.delete_sensor(data_id)
        return response, HTTPStatus.NO_CONTENT

    except Exception as e:
        if str(e) == "Inexistent_data_error":
            return {"error": "Item not found."}, HTTPStatus.NOT_FOUND

        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@data_bp.route("", methods=["GET"])
@token_required
def get_all_data():
    try:
        response = data.find_all_data()
        return response, HTTPStatus.OK

    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@data_bp.route("/<data_id>", methods=["GET"])
@token_required
def get_data(data_id):
    try:
        response = data.find_data(data_id)
        return response, HTTPStatus.OK

    except Exception as e:
        if str(e) == "Inexistent_data_error":
            return {"error": "Item not found."}, HTTPStatus.NOT_FOUND
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
