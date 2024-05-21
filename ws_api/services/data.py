from flask import request

from ..repositories import data, result
from ..utils import cammel_snake, bucket
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

    data_exists = data.find_by_id(data_id)

    if not data_exists:
        raise Exception("Inexistent_data_error")

    if user_id != str(data_exists["user_id"]):
        raise Exception("Unauthorized_error")

    bucket.delete_image(data_exists["original_image"])
    bucket.delete_image(data_exists["drawn_image"])

    data.delete(user_id, data_id)

    return {}


def create_data():
    user_id = request.environ["user_id"]

    body = request.json
    _body = cammel_snake.convert_json(body)

    # mode_exists = mode.find_by_id(_body["mode_id"], user_id)
    # if(not mode_exists):
    #    raise Exception("Mode_error")

    # TODO processar os dados
    info = _body["files"]

    # TODO info = {...}

    # TODO inserir no banco
    new_data = data.insert(user_id, info)

    result_data = {
        "data_id": new_data.inserted_id,
        "mode_id": _body["mode_id"],
        "name": _body["name"],
        "cover": _body["files"][0],
        "location": _body["location"],
    }

    new_result = result.insert(user_id, result_data)

    return {"resultId": str(new_result.inserted_id)}


# TODO Se mode_id e files não forem iguais, refazer result + data (POST)
def update_data():
    return {}
