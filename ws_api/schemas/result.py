from marshmallow import Schema, fields, validate

InfoResultSchema = Schema.from_dict(
    {
        "mode": fields.Integer(
            required=True,
            allow_none=False,
            validate=[
                validate.Range(
                    min=0, max=3, error="Boundry error: value must be between 0 and 3"
                )
            ],
        ),
        "yLabel": fields.String(required=True, allow_none=False),
        "xLabel": fields.String(required=True, allow_none=False),
        "replicateNum": fields.Integer(required=True, allow_none=False),
        "xValues": fields.List(fields.Number(), required=True, allow_none=False),
        "channels": fields.List(
            fields.String(validate=validate.OneOf(["RGB", "CMYK", "HSV", "E"])),
            allow_none=False,
        ),
    }
)

ResultBodySchema = Schema.from_dict(
    {
        "name": fields.String(required=True, allow_none=False),
        "location": fields.String(required=True, allow_none=False),
        "dataId": fields.String(required=True, allow_none=False),
        "infoResult": fields.Nested(InfoResultSchema),
    }
)
