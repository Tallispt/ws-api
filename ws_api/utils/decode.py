from bcrypt import checkpw, hashpw, gensalt
from flask import json
from bson import json_util


def parse_json(data):
    parsed_data = json.loads(json_util.dumps(data))
    if parsed_data:
        return parsed_data
    else:
        return None


def parse_bytes(str):
    return bytes(str, encoding="utf-8")


def encode_password(password):
    return hashpw(parse_bytes(password), gensalt()).decode("utf-8")


def check_password_parity(password, user_password):
    return checkpw(parse_bytes(password), parse_bytes(user_password))
