from flask_restful import Resource, request
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import make_response
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from models import GroupModel, UserModel
from validators import GroupSchema, NewGroupSchema, UpdateGroupSchema
from validators import NotFoundError, ServerError, CustomValidationError
import os

blp = Blueprint("groups", __name__, description="Operations on groups")

@blp.route("/<int:group_id>")
class Group(MethodView):
    @blp.response(200, GroupSchema)
    def get(self, group_id):
        try:
            print(f"Getting group with ID: {group_id}...")
            group = GroupModel.get_group_by_id(group_id)
            if group:
                print(f"Found group with ID {group_id}: {group}")
                return group.json(), 200
            else:
                print(f"Group with ID {group_id} not found")
                raise NotFoundError(f"Group with ID {group_id} not found")
        except NotFoundError as e:
            return make_response(e.error_response, e.code)
        except Exception as e:
            print("Error: ", e)
            raise ServerError("Error getting group")

@blp.route("/user/<int:user_id>")
class UserGroupList(MethodView):
    @blp.response(200)
    def get(self, user_id):
        try:
            print(f"Get groups with for user with id {user_id}")
            groups = GroupModel.get_groups_by_user_id(user_id)
            if groups:
                groups = [group.json() for group in groups]
                return groups, 200
            else:
                raise NotFoundError(f"No groups for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return make_response(e.error_response)
        except Exception as e:
            print("Error: ", e)
            raise ServerError("Error getting groups")
        
        
    @blp.response(201)
    @blp.arguments(NewGroupSchema, as_kwargs=True)
    def post(self, user_id, **data):
        try:
            print(f"Creating group for user with id {user_id}")
            if not UserModel.find_by_id(user_id):
                return make_response({"message": f"User with id {user_id} not found"}, 404)
            group = GroupModel(user_id, **data)
            group.save_to_db()
            print(f"Group created with id {group.id}")
            return group.json(), 201
        except CustomValidationError as e:
            print(e)
            return make_response(e.error_response, e.code)
        except Exception as e:
            print("Error: ", e)
            raise ServerError("Error creating group")
        
@blp.route("/all/user/<int:user_id>")
class UserGroupNestedDetails(MethodView):
    # Get all groups and its categories, and alarms for a user with the provided id
    def get(self, user_id):
        try:
            print(f"Get all groups' and nested details for user with id {user_id}")
            if not UserModel.find_by_id(user_id):
                return make_response({"message": f"User with id {user_id} not found"}, 404)
            groupsData = GroupModel.get_nested_group_data_by_user_id(user_id)
            if groupsData:
                print(f"Found groups' and nested details for user with id {user_id}")
                return groupsData, 200
            else:
                raise NotFoundError(f"No data for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return make_response(e.error_response)
        except Exception as e:
            print("Error: ", e)
            raise ServerError("Error getting data")

@blp.route("/<int:group_id>/user/<int:user_id>")
class UserGroup(MethodView):
    @blp.response(200, GroupSchema)
    def get(self, group_id, user_id):
        try:
            group = GroupModel.get_group_by_id_and_user_id(group_id, user_id)
            if group:
                print(f"Get group with id {group_id} for user with id {user_id}")
                return group.json()
            else:
                raise NotFoundError(f"Sound with id {group_id} not found for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting group")






