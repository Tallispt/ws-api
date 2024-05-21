from http import HTTPStatus
from flask import Blueprint
from functools import partial

from ..services import session
from ..middlewares.validation import validate_body
from ..schemas.user import SignInSchema

session_bp = Blueprint("session", __name__, url_prefix="/session")

validate = partial(validate_body, schema=SignInSchema)


@session_bp.route("", methods=["POST"])
@validate
def post_session():

    try:
        response = session.create_session()
        return response, HTTPStatus.OK

    except Exception as e:
        if str(e) == "Login_error":
            return {"error": "Unauthorazed access!"}, HTTPStatus.UNAUTHORIZED

        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
