import bcrypt
from flask import json
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

def parse_bytes(str):
    return bytes(str, encoding='utf-8')

def check_password_parity(password, user_password):
    return bcrypt.checkpw(parse_bytes(password), parse_bytes(user_password))