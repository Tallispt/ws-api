import datetime as dt

from bson import ObjectId

from ..database import mongo


def find_all(user_id):
    return mongo.db.result.aggregate(
        [
            {"$match": {"user_id": ObjectId(user_id)}},
            {
                "$lookup": {
                    "from": "data",
                    "localField": "data_id",
                    "foreignField": "_id",
                    "as": "data",
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "name": 1,
                    "location": 1,
                    "data_id": 1,
                    "data.original_image": 1,
                    "created_at": 1,
                }
            },
        ]
    )


def find_by_id(id, user_id):
    return mongo.db.result.aggregate(
        [
            {"$match": {"_id": ObjectId(id), "user_id": ObjectId(user_id)}},
            {
                "$lookup": {
                    "from": "data",
                    "localField": "data_id",
                    "foreignField": "_id",
                    "as": "data",
                }
            },
            {
                "$project": {
                    "user_id": 0,
                    "data_id": 0,
                    "data.user_id": 0,
                    "data.created_at": 0,
                }
            },
        ]
    )


def insert(user_id, data_id, name, location, result_info, result_data):
    return mongo.db.result.insert_one(
        {
            "user_id": ObjectId(user_id),
            "data_id": ObjectId(data_id),
            "name": name,
            "location": location,
            "result_info": result_info,
            "result_data": result_data,
            "created_at": dt.datetime.now(),
        }
    )


def update(user_id, id, name):
    return mongo.db.result.find_one_and_update(
        {"_id": ObjectId(id), "user_id": ObjectId(user_id)},
        {"$set": {"name": name, "updated_at": dt.datetime.now()}},
    )


def delete(user_id, id):
    return mongo.db.result.find_one_and_delete(
        {"_id": ObjectId(id), "user_id": ObjectId(user_id)}
    )
