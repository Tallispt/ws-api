from marshmallow import Schema, fields

PageBodySchema = Schema.from_dict({
    "name": fields.String(required=True, allow_none=False),
    "icon": fields.String(required=True, allow_none=False),
    "route": fields.String(required=True, allow_none=False)
})

PageSchema = Schema.from_dict({
    "_id": fields.UUID(),
    "name": fields.String(),
    "icon": fields.String(),
    "route": fields.String()
})