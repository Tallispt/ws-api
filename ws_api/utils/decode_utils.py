from flask import json
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

def parse_bytes(str):
    return bytes(str, encoding='utf-8')