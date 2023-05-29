from marshmallow import Schema, fields

DataBodySchema = Schema.from_dict({
    "name": fields.String(required=True, allow_none=False),
    "file": fields.String(required=True, allow_none=False)
})

DataSchema = Schema.from_dict({
    "_id": fields.UUID(),
    "name": fields.String(),
    "file": fields.String(),
    "created_at": fields.DateTime()
})

