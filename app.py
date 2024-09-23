from flask import Flask, jsonify, send_from_directory
# from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_smorest import Api
# from flask_swagger_ui import get_swaggerui_blueprint
from datetime import timedelta
from werkzeug.exceptions import HTTPException # for custom exceptions #

import os
from db import db, check_connection
from env import PORTAL_CONFIG_STRING
#from models import UserModel # for testing the database connection
from resources import User
from resources import Alarm
from resources import UserCategory


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

#CONFIGRATIONS FOR THE APPLICATION; SWAGGER AND DATABASE
class Config:
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", PORTAL_CONFIG_STRING)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ###------------JWT CONFIGS-------------###
    JWT_SECRET_KEY = "super-secret"  # JWT_SECRET_KEY = str(secrets.SystemRandom().getrandbits(128))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES =  timedelta(hours=20)
    ###------------SWAGGER CONFIGS-------------###
    API_TITLE = "Alarm Grouper API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.1.0"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/api/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # Additional OpenAPI specification options
    API_SPEC_OPTIONS = {
        'security': [{"bearerAuth": []}],
        'components': {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }





### --------------OLD DATABASE SETUP------------------- ###
# #CONFIGURES THE SQLALCHEMY DATA BASE CONNECTION
# app.config['SQLALCHEMY_DATABASE_URI'] = PORTAL_CONFIG_STRING
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db.init_app(app)
### --------------OLD DATABASE SETUP------------------- ###

app.config.from_object(Config)
db.init_app(app)

api = Api(app)

jwt = JWTManager(app)

socketio = SocketIO(app, cors_allowed_origins='*')

# @app.route('/static/swagger.yaml')
# def swagger_yaml():
#     return send_from_directory(os.getcwd(), 'swagger.yaml')

@app.errorhandler(HTTPException)
def handle_root_exception(error):
    return {
        'message': error.message if hasattr(error, 'message') else 'An error occurred',
        'status': error.code,
        'description': error.description,
    }, error.code


### --------------REGISTER ENDPOINTS------------------- ###
api.register_blueprint(User, url_prefix='/api/users')

api.register_blueprint(Alarm, url_prefix='/api/alarms')

api.register_blueprint(UserCategory, url_prefix='/api/categories')
### --------------REGISTER ENDPOINTS END------------------- ###


# def process_user():
#     try:
#         user = UserModel("Candy", "candy@gmail.com", "password")
#         user.save_to_db()
#         print("User processing completed")
#     except Exception as e:
#         print(e)



### --------------MAIN------------------- ###
if __name__ == '__main__':
    with app.app_context():
        try:
            # Check if the process is the reloader
            if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
                # print("Creating tables...")
                # db.create_all()
                # print("Checking database connection...")
                check_connection()
                # print("Processing user...")
                # process_user()
        except Exception as e:
            print(f"Error during startup: {e}")
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)


