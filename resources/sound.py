from flask_restful import Resource, request
from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from models import SoundModel
from validators import NotFoundError, ServerError, CustomValidationError
from werkzeug.utils import secure_filename
import os, pathlib

blp = Blueprint("sounds", __name__, description="Operations on sounds")

@blp.route("/")
class SoundList(MethodView):
    @blp.response(200)
    def get(self):
        try:
            print("Getting default sounds...")
            sounds = SoundModel.get_all_sounds()
            if sounds:
                return [sound.json() for sound in sounds]
            else:
                return {"message": "No sounds found"}, 200
        except Exception as e:
            raise ServerError("Error getting sounds")
        
    @blp.response(201)
    def post(self):
        try:
            print("Adding new sound...")
            data = request.get_json()
            # Retrieve the text fields
            name = data.get('name')
            file = data.get('file')
            description = data.get('description')
            user_id = data.get('user_id')
            sound = SoundModel(user_id, name, file, description)
            if sound:
                sound.save_to_db()
                print(f"Name: {name}, Description: {file}, User ID: {user_id}, is adding a new sound...")
                return {"message": "Sound added successfully"}, 201
        except CustomValidationError as e:
            return e.error_response, e.code
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error adding sound")

@blp.route("/<int:sound_id>")
class Sound(MethodView):
    @blp.response(200)
    def get(self, sound_id):
        try:
            sound = SoundModel.get_sound_by_id(sound_id)
            if sound:
                print(f"Found sound with ID {sound_id}: {sound}")
                return sound.json(), 200
            else:
                print(f"Sound with ID {sound_id} not found")
                raise NotFoundError(f"Sound with ID {sound_id} not found")
        except NotFoundError as e:
            return e.error_response, e.code
        except CustomValidationError as e:
            return e.error_response, e.code
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting sound")

@blp.route("/user/<int:user_id>")
class UserSoundList(MethodView):
    @blp.response(200)
    def get(self, user_id):
        try:
            print(f"Get sounds for user with id {user_id}")
            sounds = SoundModel.get_sounds_by_user_id(user_id)
            if sounds:
                sounds = [sound.json() for sound in sounds]
                return {"message": f"found sounds for user with id {user_id}", "sounds": sounds}, 200
            else:
                raise NotFoundError(f"No sound for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return e.error_response, e.code
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting sounds for user")

@blp.route("/<int:sound_id>/user/<int:user_id>")
class UserSound(MethodView):
    @blp.response(200)
    def get(self, sound_id, user_id):
        try:
            sound = SoundModel.get_sound_by_id_and_user_id(sound_id, user_id)
            if sound:
                print(f"Get sound with id {sound_id} for user with id {user_id}")
                return sound.json()
            else:
                raise NotFoundError(f"Sound with id {sound_id} not found for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return e.error_response, e.code
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting alarm")






