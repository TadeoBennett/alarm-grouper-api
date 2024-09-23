from flask import request
from flask_restful import Resource
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from models.user import UserModel
from validators import CustomValidationError, ServerError
from validators import UserSchema, NewUserSchema
from flask_bcrypt import generate_password_hash

from validators.errors import EmailExistsError

# newUserSchema = UserSchema()

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route('/')
class UserListResource(MethodView):
    # get all users
    @blp.response(201)
    def get(self):
        try:
            return [user.json() for user in UserModel.get_all()]
        except Exception as e:
            print("Error: ", e)
            raise ServerError

    @blp.arguments(NewUserSchema)
    @blp.response(200)
    def post(self, user_data):
        try:
            if UserModel.find_by_email(user_data['email']):
                raise EmailExistsError(user_data['email'])
            user = UserModel(**user_data)
            user.save_to_db()
            return user.json()
        except EmailExistsError as e:
            print("Error: ", e)
            return {"Error": e.message, "code": e.code, "message": e.description}, e.code
        except Exception as e:
            print("Error: ", e)
            raise ServerError

@blp.route('/<int:user_id>')
class UserResource(MethodView):
    @blp.response(200)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user.json()