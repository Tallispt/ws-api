from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.Str(required=True, allow_none=False)
    email = fields.Email()
    password = fields.UUID()