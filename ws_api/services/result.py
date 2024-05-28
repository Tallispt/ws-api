from bson import json_util
from flask import g, request
from marshmallow import ValidationError

from ..repositories import data, result
from ..services import data as data_service
from ..utils import cammel_snake
from ..utils import data_manipulator as dm
from ..utils import image_manipulator as im
from ..utils.image_class import Image


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

    result_data = result.find_by_id(id, user_id)

    if not result_data:
        raise Exception("Not_found_error")

    response = json_util.dumps(result_data)

    return response


def create_result():
    user_id = request.environ["user_id"]
    body = request.json

    name = body["name"]
    location = body["location"]
    data_id = body["dataId"]
    mode = int(body["infoResult"]["mode"])
    replicate_num = int(body["infoResult"]["replicateNum"])
    sample_num = int(body["infoResult"]["sampleNum"])
    x_values_len = len(body["infoResult"]["xValues"])
    channels = body["infoResult"]["channels"]
    info_result = {
        "mode": mode,
        "yLabel": body["infoResult"]["yLabel"],
        "xLabel": body["infoResult"]["xLabel"],
        "replicateNum": replicate_num,
        "sampleNum": sample_num,
        "xValues": [float(i) for i in body["infoResult"]["xValues"]],
        "channels": channels,
    }

    if sample_num != x_values_len:
        raise ValidationError("Number of samples not matching from x Values")

    existing_data = data_service.find_data(data_id)

    if not existing_data:
        raise Exception("Inexistent_data_error")

    existing_data = json_util.loads(existing_data)

    original_image = existing_data["original_image"]
    detected_circles = existing_data["detected_circles"]

    if x_values_len * replicate_num != len(detected_circles):
        raise Exception("Given number of spots do not match the number of detections")

    image = Image(original_image)
    values = im.av_value(detected_circles, image, mode)

    result_data = dict()

    for channel in channels:
        new_values = dm.convert_colors(values, channel)

        spots_df = dm.create_spots_df(new_values, channel)

        replicate_df = dm.create_replicates_df(
            new_values, info_result, channel, len(channel)
        )

        mean_df = dm.create_avs_df(replicate_df)

        regression_df, plot_regressions_df = dm.create_regressions_df(mean_df, channel)

        result_data[channel] = {
            "spots": spots_df.to_dict("records"),
            "replicatas": replicate_df.to_dict("records"),
            "means": mean_df.to_dict("records"),
            "regressions": regression_df.to_dict("records"),
            "plot_means": mean_df.to_dict("list"),
            "plot_regressions": plot_regressions_df.to_dict("records"),
        }

    inserted_result = result.insert(
        user_id, data_id, name, location, info_result, result_data
    )
    print("oi")

    return {"id": str(inserted_result.inserted_id)}


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
    data.delete(user_id, deleted_result["data_id"])

    return {}
