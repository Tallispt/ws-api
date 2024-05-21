from marshmallow import Schema, fields

DetectFormsBodySchema = Schema.from_dict(
    {
        "kernel": fields.String(required=True, allow_none=False),
        "minDist": fields.String(required=True, allow_none=False),
        "param1": fields.String(required=True, allow_none=False),
        "param2": fields.String(required=True, allow_none=False),
        "minRadius": fields.String(required=True, allow_none=False),
        "maxRadius": fields.String(required=True, allow_none=False),
        "radiusPercent": fields.String(required=True, allow_none=False),
    }
)
