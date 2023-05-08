from marshmallow import Schema, fields

SessionSchema = Schema.from_dict({
    "_id": fields.UUID(allow_none=True),
    "user_id": fields.UUID(allow_none=True),
    "token": fields.String(required=True),
    "is_valid": fields.Boolean(required=True),
    "created_at": fields.DateTime(allow_none=True)
})