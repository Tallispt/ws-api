from bson import json_util
from flask import request

from ..repositories import data, result
from ..utils import bucket, cammel_snake
from ..utils.image_manipulator import return_detected_circles


def detect_sensor():
    file = request.files["file"].read()
    form_data = request.form
    user_id = request.environ["user_id"]

    pts, drawn_img = return_detected_circles(file, form_data)

    img_blob = bucket.upload_image(file)
    drawn_img_blob = bucket.upload_image(drawn_img)

    original_img_url = img_blob.public_url
    drawn_img_url = drawn_img_blob.public_url
    detected_circles = pts.tolist()

    inserted_data = data.insert(
        user_id=user_id,
        original_image=original_img_url,
        drawn_image=drawn_img_url,
        detected_circles=detected_circles,
        info=form_data,
    )

    return {
        "id": str(inserted_data.inserted_id),
        "detected_circles": detected_circles,
        "originalImage": original_img_url,
        "drawnImage": drawn_img_url,
    }


def delete_sensor(data_id):
    user_id = request.environ["user_id"]

    data_exists = data.find_by_id_by_user_id(data_id, user_id)

    if not data_exists:
        raise Exception("Inexistent_data_error")

    bucket.delete_image(data_exists["original_image"])
    bucket.delete_image(data_exists["drawn_image"])

    data.delete(user_id, data_id)

    return {}


def find_all_data():
    user_id = request.environ["user_id"]

    data_data = data.find_by_user_id(user_id)

    if not data_data:
        return []

    list_cur = list(data_data)
    response = json_util.dumps(list_cur)

    return response


def find_data(id):
    user_id = request.environ["user_id"]

    existing_data = data.find_by_id_by_user_id(id, user_id)

    if not existing_data:
        raise Exception("Inexistent_data_error")

    response = json_util.dumps(existing_data)

    return response


# TODO Se mode_id e files não forem iguais, refazer result + data (POST)
def update_data():
    return {}
