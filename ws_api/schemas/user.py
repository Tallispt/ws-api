from marshmallow import Schema, fields

SignInSchema = Schema.from_dict({
    "username": fields.String(required=True, allow_none=False),
    "password": fields.String(required=True, allow_none=False)
})

SignUpSchema = Schema.from_dict({
    "username": fields.String(required=True, allow_none=False),
    "email": fields.Email(required=True, allow_none=False),
    "password": fields.String(required=True, allow_none=False)
})

UserSchema = Schema.from_dict({
    "_id": fields.UUID(),
    "username": fields.String(),
    "email": fields.Email(),
    "password": fields.String(),
    "created_at": fields.DateTime()
})