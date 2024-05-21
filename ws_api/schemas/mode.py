from marshmallow import Schema, fields

ConfigBodySchema = Schema.from_dict(
    {
        "numOfPictures": fields.Integer(required=True, allow_none=False),
        "detectBorders": fields.Boolean(required=True, allow_none=False),
        "regressionName": fields.String(required=True, allow_none=False),
        "xCoordLable": fields.String(required=True, allow_none=False),
        "xValues": fields.List(
            required=True, allow_none=False, cls_or_instance=fields.Integer()
        ),
        "yCoordLable": fields.String(required=True, allow_none=False),
        "yValues": fields.List(
            required=True, allow_none=False, cls_or_instance=fields.Integer()
        ),
        "replicatesNum": fields.Integer(),
        "delta": fields.Boolean(),
        "rgb": fields.Boolean(),
        "cmyk": fields.Boolean(),
        "hsv": fields.Boolean(),
        "eucl": fields.Boolean(),
    }
)

ModeBodySchema = Schema.from_dict(
    {
        "title": fields.String(required=True, allow_none=False),
        "type": fields.String(required=True, allow_none=False),
        "config": fields.Nested(ConfigBodySchema),
    }
)
