from flask import request, make_response
from flask_restful import Resource
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from validators import CustomValidationError, ServerError
from validators import NewUserSchema, UpdateUserSchema
from validators import EmailExistsError, NotFoundError, ServerError
from flask_bcrypt import generate_password_hash
from models import UserModel
from validators import NewUserSchema, UpdateUserSchema, UserSchema
from datetime import datetime
# newUserSchema = UserSchema()

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route('/')
class UserListResource(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        try:
            users = UserModel.get_all()
            if users:
                print("Users found")
                return [user.json() for user in users]
            else:
                print("No users found")
                return {"message": "No users found"}, 200
        except Exception as e:
            print("Error: ", e)
            raise ServerError

    @blp.arguments(NewUserSchema, as_kwargs=True)
    @blp.response(200)
    def post(self, **data):
        # NOTE: the data is already check for unique email entry and matching passwords in schema
        try:
            params = {
                "username": data.get('username'),
                "email": data.get('email'),
                "password": data.get('password'),
                "created_at": str(datetime.now())
            }
            print(params)
            user = UserModel(**params)
            if user:
                return user.json(), 201
            else:
                raise ServerError("Could not create user")
        except Exception as e:
            print("error: ", e)
        

@blp.route('/<int:user_id>')
class UserResource(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        try:
            user = UserModel.find_by_id(user_id)
            if not user:
                print(f"User with id({user_id}) not found")
                raise NotFoundError(f"User with id({user_id})")
            print(f"User with id({user_id}) found: {user.json()}")
            return user.json()
        except NotFoundError as e:
            print("Error: ", e)
            return make_response(e.error_response, e.code)
        except Exception as e:
            print("Error: ", e)
            raise ServerError
        
    # delete a user with a specific id
    @blp.response(200)
    def delete (self, user_id):
        try:
            user = UserModel.find_by_id(user_id)
            if not user:
                raise NotFoundError(f"User with id({user_id})")
            returnUser = user.json()  #save a copy of the user
            user.delete_from_db()   #delete the user from the db
            returnUser["response"] = {
                "message": "User deleted",
                "status": 200
            }
            # print(returnUser)
            return returnUser
        except NotFoundError as e:
            print("Error: ", e)
            return {"Error": e.message, "code": e.code, "message": e.description}, e.code
        except Exception as e:
            print("Error: ", e)
            raise ServerError
        
    # updating a user with a specific id
    @blp.arguments(UpdateUserSchema)
    @blp.response(200)
    def put(self, user_data, user_id):
        try:
            # check if the user exists
            user = UserModel.find_by_id(user_id)
            if not user:
                raise NotFoundError(f"User with id({user_id})")
            
            # check if the email has a value and if it is different from the existing email
            user_existing_email = user.email;
            if user_data['email'] is None or user_data['email'] == "":
                #password is not being changed
                user_data['email'] = user_existing_email
            else:
                if user_existing_email != user_data['email']: # want to change the email?
                    if UserModel.find_by_email(user_data['email']): # is the email already in use?
                        raise EmailExistsError(user_data['email'])
                else:
                    user_data['email'] = user_existing_email # keep the old email (no change)
            
            user.update_db(user_data['username'], user_data['email'])
            
            returnUser = user.json()
            returnUser["response"] = {
                "message": "User updated",
                "status": 200
            }
            return returnUser
        except EmailExistsError as e:
            return e.error_response, e.code
        except NotFoundError as e:
            return e.error_response, e.code
        except ValidationError as e:
            print("Error: ", e.messages)
            return {"errors": e.messages}, 422
        except Exception as e:
            print("Error: ", e)
            raise ServerError