from marshmallow import Schema, fields, validate

InfoResultSchema = Schema.from_dict(
    {
        "mode": fields.Integer(
            required=True,
            allow_none=False,
            validate=[validate.Range(min=0, max=3)],
        ),
        "yLabel": fields.String(required=True, allow_none=False),
        "xLabel": fields.String(required=True, allow_none=False),
        "replicateNum": fields.Integer(
            required=True,
            allow_none=False,
            validate=validate.Range(min=1, max=20),
        ),
        "sampleNum": fields.Integer(
            required=True,
            allow_none=False,
            validate=validate.Range(min=1, max=20),
        ),
        "xValues": fields.List(
            fields.Float(allow_none=False), required=True, allow_none=True
        ),
        "channels": fields.List(
            fields.String(validate=validate.OneOf(["RGB", "CMYK", "HSV", "E"])),
            allow_none=False,
        ),
    }
)

ResultBodySchema = Schema.from_dict(
    {
        "name": fields.String(required=True, allow_none=False),
        "location": fields.String(required=True, allow_none=True),
        "dataId": fields.String(required=True, allow_none=False),
        "infoResult": fields.Nested(InfoResultSchema),
    }
)
