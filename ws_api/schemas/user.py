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