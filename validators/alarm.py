from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from models import CategoryModel
from validators import CustomValidationError
from marshmallow import Schema, fields, validate
import re

class BaseAlarmSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    description = fields.String(required=False, allow_none=True)
    ringTime = fields.String(required=True, allow_none=True, validate=validate.Length(min=1, max=50))
    ringDate = fields.String(required=True, allow_none=True, validate=validate.Length(min=1, max=50))
    repeat = fields.Boolean(required=True)
    sound_id = fields.Integer(required=True, validate=validate.Range(min=1))
    active = fields.Boolean(required=True)

class AlarmSchema(BaseAlarmSchema):
    id = fields.Integer(validate=validate.Range(min=1), dump_only=True)    
    alarm_creator_id = fields.Integer(required=True, validate=validate.Range(min=1))
    category_id = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))
    created_at = fields.DateTime(dump_only=True)
    
class UpdateAlarmSchema(BaseAlarmSchema):
    category_id = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))

class NewAlarmSchema(BaseAlarmSchema):
    category_id = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))


# Custom validators for time and date formats
def validate_time(value):
    if not re.match(r'^\d{2}:\d{2}$', value):
        raise ValidationError("Time must be in the format HH:MM (24-hour).")

def validate_date(value):
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', value):
        raise ValidationError("Date must be in the format dd/mm/yyyy.")
