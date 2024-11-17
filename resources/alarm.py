from flask_restful import Resource, request
from flask_smorest import Blueprint
from flask import make_response
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from models import AlarmModel, UserModel
from validators import NotFoundError, ServerError, CustomValidationError
from validators import BaseAlarmSchema, AlarmSchema, UpdateAlarmSchema, NewAlarmSchema
import os
from datetime import datetime


blp = Blueprint("alarms", __name__, description="Operations on alarms")

@blp.route("/<int:alarm_id>")
class Alarm(MethodView):
    @blp.response(200, AlarmSchema)
    def get(self, alarm_id):
        try:
            alarm = AlarmModel.get_alarm_by_id(alarm_id)
            if alarm:
                print(f"Found alarm with ID {alarm_id}: {alarm}")
                return alarm.json(), 200
            else:
                print(f"Alarm with ID {alarm_id} not found")
                raise NotFoundError(f"Alarm with ID {alarm_id} not found")
        except NotFoundError as e:
            return make_response(e.error_response, e.code)
        except CustomValidationError as e:
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting alarm")

@blp.route("/user/<int:user_id>")
class AlarmList(MethodView):
    @blp.response(200, AlarmSchema(many=True))
    def get(self, user_id):
        try:
            print(f"Get alarms for user with id {user_id}")
            alarms = AlarmModel.get_alarms_by_user_id(user_id)
            if alarms:
                alarms = [alarm.json() for alarm in alarms]
                return alarms, 200
            else:
                raise NotFoundError(f"No alarm for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting alarms for user")
        
    @blp.response(201)
    @blp.arguments(NewAlarmSchema, as_kwargs=True)
    def post(self, user_id, **data):
        try:
            print(f"Adding new alarm for user with id {user_id}")
            if not UserModel.find_by_id(user_id):
                print(f"User with id {user_id} not found")
                return make_response({"message": f"User with id {user_id} not found"}, 404)
            params = {
                "alarm_creator_id" : user_id,
                "category_id" : data.get("category_id"),
                "name" : data.get("name"),
                "description" : data.get("description"),
                "ringTime" : data.get("ringTime"),
                "ringDate" : data.get("ringDate"),
                "repeat" : data.get("repeat"),
                "sound_id" : data.get("sound_id"),
                "active" : data.get("active"),
                "created_at" : datetime.now()
            }
            
            try:
                params["category_id"] = int(params["category_id"])
                params["repeat"] = bool(params["repeat"])
                params["sound_id"] = int(params["sound_id"])
                params["active"] = bool(params["active"])
                if params["description"] == '':
                    params["description"] = None
                if params["ringTime"] == '':
                    params["ringTime"] = None
                if params["ringDate"] == '':
                    params["ringDate"] = None
            except (TypeError, ValueError) as e:
                print("Error", e)
                raise CustomValidationError("Invalid data types provided for alarm") from e
            
            alarm = AlarmModel(**params)
            if alarm:
                alarm.save_to_db()
                return {"message": "Alarm added successfully", "data": alarm.json()}, 201
            else:
                raise ServerError("Failed to add alarm")
        except CustomValidationError as e:
            return make_response(e.error_response, e.code)
        except ServerError as e:
            print(f"Error: {str(e)}")
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Failed to add alarm: {str(e)}")
            raise ServerError("Failed to add alarm")

@blp.route("/<int:alarm_id>/user/<int:user_id>")
class UserAlarm(MethodView):
    @blp.response(200, AlarmSchema)
    def get(self, alarm_id, user_id):
        try:
            alarm = AlarmModel.get_alarm_by_id_and_user_id(alarm_id, user_id)
            if alarm:
                print(f"Get alarm with id {alarm_id} for user with id {user_id}")
                return alarm.json()
            else:
                raise NotFoundError(f"Alarm with id {alarm_id} not found for user with id {user_id}")
        except NotFoundError as e:
            print(e)
            return make_response(e.error_response, e.code)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ServerError("Error getting alarm for user")