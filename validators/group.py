from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from models import CategoryModel
from validators import CustomValidationError
from marshmallow import Schema, fields, validate
import re

class BaseGroupSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    description = fields.String(required=False, validate=validate.Length(min=1, max=100), allow_none=True)

class GroupSchema(BaseGroupSchema):
    id = fields.Integer(required=True, validate=validate.Range(min=1))
    group_creator_id = fields.Integer(required=True, validate=validate.Range(min=1))

    created_at = fields.DateTime(dump_only=True)

class UpdateGroupSchema(BaseGroupSchema):
    pass

class NewGroupSchema(BaseGroupSchema):
    pass