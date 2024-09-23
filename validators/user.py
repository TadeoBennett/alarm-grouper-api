from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from models import UserModel
import re

class UserSchema(Schema):
    id =  fields.Integer( validate=validate.Range(min=1))
    username = fields.String(required=True, validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True, validate=validate.Length(max=80))
    password = fields.String(required=True, validate=validate.Length(max=256))
    created_at = fields.DateTime(required=True)

class NewUserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True, validate=validate.Length(max=80))
    password = fields.String(required=True, validate=validate.Length(min=6))

    # @validates_schema
    # def validate_user_schema(self, data, **kwargs):
    #     #validate email
    #     user_by_email = UserModel.find_by_email(data["email"])
    #     if user_by_email: #if a user exizsts with that email
    #         if user_by_email.id != data["id"]: #if a different user exists with the that email
    #             raise ValidationError({"message": f'Another user exist with same Email: {data["email"]}'})
    #     #validate password
    #     if not re.match(r'^[a-zA-Z0-9!@#$%^&*()\-_=+\[\]{}|;:\'",.<>?/`~]+$', data["password"]):
    #         raise ValidationError({"message": "Password contains invalid characters."})