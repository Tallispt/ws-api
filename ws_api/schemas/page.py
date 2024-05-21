from marshmallow import Schema, fields

PageBodySchema = Schema.from_dict(
    {
        "name": fields.String(required=True, allow_none=False),
        "icon": fields.String(required=True, allow_none=False),
        "route": fields.String(required=True, allow_none=False),
    }
)
