from flask import Blueprint

data_bp = Blueprint("data", __name__, url_prefix="/data")

# TODO Data routers

# @data_bp.route('', methods=['GET'])
# def get_data():
#   data = mongo.db.data.find()
#   print(len(list(get_data)))
#   return make_response(json_util.dumps({'page' : data}),
#     mimetype='application/json')

# @data_bp.route('', methods=['POST'])
# def create_data():
#   data = request.get_json()
#   post_data = mongo.db.data.insert_one(data)
#   print(post_data)
#   return "OK"