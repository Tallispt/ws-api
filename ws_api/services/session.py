from datetime import datetime, timedelta

import jwt
from flask import request

from ..loadenv import config
from ..repositories import user
from ..utils.decode import check_password_parity


def create_session():
    username, password = request.json.values()

    db_user = user.find_by_username(username)

    if not db_user:
        db_user = user.find_by_email(username)
    if not db_user:
        raise Exception("Login_error")

    db_id, db_username, _, db_password, _ = db_user.values()
    check = check_password_parity(password, db_password)

    if not check:
        raise Exception("Login_error")

    token = jwt.encode(
        {
            "username": db_username,
            "userId": str(db_id),
            "expiration": str(datetime.utcnow() + timedelta(days=2)),
        },
        config["JWT_SECRET_KEY"],
    )

    return {"username": db_username, "userId": str(db_id), "token": token}


def auth_session(token):
    if not token:
        raise Exception("Unauthorized_access_error")

    username, user_id, expiration = jwt.decode(
        token, config["JWT_SECRET_KEY"], algorithms=["HS256"]
    ).values()

    date_exp = datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S.%f")
    date_now = datetime.utcnow()

    if date_exp < date_now:
        raise Exception("Unauthorized_access_error")

    db_user = user.find_by_id(user_id)

    if not db_user or db_user["username"] != username:
        raise Exception("Unauthorized_access_error")

    return user_id
