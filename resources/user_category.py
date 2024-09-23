from flask_restful import Resource
from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

blp = Blueprint("UserCategories", __name__, description="Operations on categories")

@blp.route("/")
class UserCategoryListResource(MethodView):
    # @jwt_required()
    @blp.response(200)
    def get(self):
        return {
            "message": "Get Categories"
        }

    @blp.response(200)
    def post(self):
        return {
            "message": "Post Categories"
        }