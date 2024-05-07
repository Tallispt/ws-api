from marshmallow import Schema, fields

DetectFormsBodySchema = Schema.from_dict({
    "kernel": fields.String(required=True, allow_none=False),
    "minDist": fields.String(required=True, allow_none=False),
    "param1": fields.String(required=True, allow_none=False),
    "param2": fields.String(required=True, allow_none=False),
    "minRadius": fields.String(required=True, allow_none=False),
    "maxRadius": fields.String(required=True, allow_none=False),
    "radiusPercent": fields.String(required=True, allow_none=False)
})

DetectDelBodySchema = Schema.from_dict({
    "originalImage": fields.Url(required=True, allow_none=False),
    "drawnImage": fields.Url(required=True, allow_none=False)
})

DataBodySchema = Schema.from_dict({
    "modeId": fields.String(required=True, allow_none=False),
    "name": fields.String(required=True, allow_none=False),
    "location": fields.String(required=True, allow_none=False),
    "files": fields.List(required=True, allow_none=False, cls_or_instance=fields.String())
})
