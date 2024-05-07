from flask import request

from ..repositories import data, result, mode
from ..utils import cammel_snake, bucket
from ..utils.image_manipulator import return_detected_circles

def detect_sensor():
  file = request.files['file'].read()
  form = request.form

#TODO Transform multiple parameters into dictionaty
  pts, drawn_img = return_detected_circles(
    file,
    kernel = (int(form['kernel']), int(form['kernel'])),
    min_dist = int(form['minDist']),
    param_1 = int(form['param1']),
    param_2 = int(form['param2']),
    min_radius = int(form['minRadius']),
    max_radius = int(form['maxRadius']),
    radius_percent = int(form['radiusPercent'])
    )

  img_blob = bucket.upload_image(file)
  drawn_img_blob = bucket.upload_image(drawn_img)

  return {
    'detected_circles': pts.tolist(), 
    'originalImage': img_blob.public_url, 
    'drawnImage': drawn_img_blob.public_url
    }

def delete_sensor():
  body = request.json

  bucket.delete_image(body['originalImage'])
  bucket.delete_image(body['drawnImage'])

  return {}

def create_data():
  user_id = request.environ['user_id']

  body = request.json
  _body = cammel_snake.convert_json(body)

  mode_exists = mode.find_by_id(_body["mode_id"], user_id)
  if(not mode_exists):
     raise Exception("Mode_error")

  #TODO processar os dados
  info = _body["files"]

  #TODO info = {...}

  #TODO inserir no banco
  new_data = data.insert(user_id, info)

  result_data = {
    "data_id": new_data.inserted_id,
    "mode_id": _body["mode_id"],
    "name": _body["name"],
    "cover": _body["files"][0],
    "location": _body["location"]
  }

  new_result = result.insert(user_id, result_data)

  return {"resultId": str(new_result.inserted_id)}

#TODO Se mode_id e files não forem iguais, refazer result + data (POST)
def update_data():
  return {}