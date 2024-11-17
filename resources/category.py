from flask_restful import Resource, request
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import make_response
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from validators import NotFoundError, ServerError, CustomValidationError
from models import CategoryModel, UserModel
from validators import BaseCategorySchema, CategorySchema, UpdateCategorySchema, NewCategorySchema
from datetime import datetime
import os

blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        try:
            category = CategoryModel.get_category_by_id(category_id)
            if category:
                print(f"Found category with ID {category_id}: {category}")
                return category.json(), 200
            else:
                print(f"Category with ID {category_id} not found")
                raise NotFoundError(f"Category with ID {category_id} not found")
        except NotFoundError as e:
            return make_response(e.error_response, e.code)
        except CustomValidationError as e:
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting category")

@blp.route("/user/<int:user_id>")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self, user_id):
        try:
            print(f"Get categories for user with id {user_id}")
            categories = CategoryModel.get_categories_by_user_id(user_id)
            if categories:
                categories = [category.json() for category in categories]
                return categories, 200
            else:
                raise NotFoundError(f"No categories for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting categories for user")
    
    @blp.response(201)
    @blp.arguments(NewCategorySchema, as_kwargs=True)
    def post(self, user_id, **data):
        print(f"Create new category for user with id {user_id}")
        if not UserModel.find_by_id(user_id):
            print(f"User with id {user_id} not found")
            return make_response({"message": f"User with id {user_id} not found"}, 404)
        data = request.get_json()
        params = {
            "category_creator_id" : user_id,
            "group_id" : data.get("group_id"),
            "name" : data.get("name"),
            "description" : data.get("description"),
            "created_at" : str(datetime.now())
        }
        
        try:
            params["group_id"] = int(params["group_id"])
        except (TypeError, ValueError) as e:
            print("Error: ", e)
            raise CustomValidationError("Invalid data types (group_id) for category", 400)
        
        try:
            category = CategoryModel(**params)
            if category:
                category.save_to_db()
                return {"message": "Category created successfully", "data": category.json()}, 201
            else:
                raise ServerError("Error creating category")
        except CustomValidationError as e:
            return make_response(e.error_response, e.code)
        except ServerError as e:
            print("Error", e)
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error creating category")

@blp.route("/<int:category_id>/user/<int:user_id>")
class UserCategory(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id, user_id):
        try:
            category = CategoryModel.get_category_by_id_and_user_id(category_id, user_id)
            if category:
                print(f"Get category with id {category_id} for user with id {user_id}")
                return category.json()
            else:
                raise NotFoundError(f"Category with id {category_id} not found for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting category for user")