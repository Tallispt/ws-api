import cv2
import uuid
import numpy as np
from .image_class import Image
from firebase_admin import storage


def upload_image(file):
    file = Image(file)
    img_encode = cv2.imencode(".jpg", file.image)[1]
    data_encode = np.array(img_encode)
    file = data_encode.tobytes()

    uuid_name = uuid.uuid4()
    bucket = storage.bucket()
    blob = bucket.blob(f"{uuid_name}.jpg")

    blob.upload_from_string(file, content_type="image/jpg")
    blob.make_public()

    return blob


def delete_image(img_url):
    img_name = img_url.split("/")[-1]

    bucket = storage.bucket()
    image = bucket.get_blob(img_name)

    if image is None:
        # TODO Write exception type here
        raise Exception()
    image.delete()
