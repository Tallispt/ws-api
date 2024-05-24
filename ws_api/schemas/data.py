from marshmallow import Schema, ValidationError, fields, validate


def is_odd(value):
    if value % 2 == 0:
        raise ValidationError("Not an even value.")


DetectFormsBodySchema = Schema.from_dict(
    {
        "kernel": fields.Integer(
            required=True,
            allow_none=False,
            validate=validate.And(validate.Range(min=3), is_odd),
        ),
        "minDist": fields.Integer(
            required=True, allow_none=False, validate=validate.Range(min=1, max=200)
        ),
        "param1": fields.Integer(
            required=True, allow_none=False, validate=validate.Range(min=1, max=200)
        ),
        "param2": fields.Integer(
            required=True, allow_none=False, validate=validate.Range(min=1, max=200)
        ),
        "minRadius": fields.Integer(
            required=True, allow_none=False, validate=validate.Range(min=1, max=200)
        ),
        "maxRadius": fields.Integer(
            required=True, allow_none=False, validate=validate.Range(min=1, max=200)
        ),
        "radiusPercent": fields.Integer(
            required=True, allow_none=False, validate=validate.Range(min=1, max=150)
        ),
        "sortingType": fields.String(
            required=True,
            allow_none=True,
            default="h",
            validate=validate.OneOf(["h", "v"]),
        ),
    }
)
