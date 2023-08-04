from marshmallow import Schema, fields

DetectSchema = Schema.from_dict({
    "file": fields.String(required=True, allow_none=False)
})

DataBodySchema = Schema.from_dict({
    "file": fields.String(required=True, allow_none=False)
})

DataSchema = Schema.from_dict({
    "_id": fields.UUID(),
    "name": fields.String(),
    "file": fields.String(),
    "created_at": fields.DateTime()
})
