from flask import Blueprint
from http import HTTPStatus

health_bp = Blueprint("health", __name__, url_prefix="/health")


@health_bp.route("", methods=["GET"])
def health():
    return {}, HTTPStatus.OK
