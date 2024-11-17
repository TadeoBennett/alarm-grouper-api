from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from models import CategoryModel
from validators import CustomValidationError
from marshmallow import Schema, fields, validate
import re


class BaseCategorySchema(Schema):
    group_id = fields.Integer(required=True, validate=validate.Range(min=1))
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    description = fields.String(required=False, allow_none=True, validate=validate.Length(min=1, max=100))
    
class CategorySchema(BaseCategorySchema):
    id = fields.Integer(validate=validate.Range(min=1), dump_only=True)
    category_creator_id = fields.Integer(required=True, validate=validate.Range(min=1))
    created_at = fields.DateTime(dump_only=True)
    
class UpdateCategorySchema(BaseCategorySchema):
    pass

class NewCategorySchema(BaseCategorySchema):
    pass