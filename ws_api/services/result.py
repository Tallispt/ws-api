from flask import request
from bson import json_util

from ..services import data as data_service
from ..repositories import result, data
from ..utils import cammel_snake


def find_all_results():
    user_id = request.environ["user_id"]

    result_data = result.find_all(user_id)

    if not result_data:
        return []

    list_cur = list(result_data)
    response = json_util.dumps(list_cur)

    return response


def find_result(id):
    user_id = request.environ["user_id"]

    result_data = result.find_by_id(user_id, id)

    if not result_data:
        raise Exception("Not_found_error")

    response = json_util.dumps(result_data)

    return response


def create_result():
    return {}


def update_result(id):
    user_id = request.environ["user_id"]

    body = request.json
    _body = cammel_snake.convert_json(body)

    result_exists = result.find_by_id(user_id, _body["_id"])

    if not result_exists:
        return Exception("Not_found_error")

    if (result_exists["mode_id"] != _body["mode_id"]) or (
        result_exists["files"] != _body["files"]
    ):
        # TODO Se mode_id e files não forem iguais, refazer result + data (POST)
        return data_service.update_data()

    updated_result = result.update(user_id, id, _body["name"])
    return {"resultId": str(updated_result["_id"])}


def remove_result(id):
    user_id = request.environ["user_id"]

    deleted_result = result.delete(user_id, id)
    deleted_data = data.delete(user_id, deleted_result["data_id"])

    return {"resultId": str(deleted_result["_id"]), "dataId": str(deleted_data["_id"])}
