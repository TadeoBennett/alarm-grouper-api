from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

# import mysql.connector
# from mysql.connector import Error

from env import PORTAL_CONFIG_STRING

db = SQLAlchemy()

# def get_db_connection():
#     return mysql.connector.connect(**PORTAL_CONFIGS)


def get_sql_alchemy_db_connection():
    print("Connecting to the database...: ", PORTAL_CONFIG_STRING)
    return PORTAL_CONFIG_STRING


def check_connection():
    try:
        # Create a new session
        with db.session.begin():
            # Execute a simple query to check the connection
            result = db.session.execute(text("SELECT 1"))
            print("Connection to MySQL database was successful!")

            # Optionally, you can query the database for tables
            tables = db.session.execute(text("SHOW TABLES")).fetchall()
            print("Tables in the database:", tables)

    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
    finally:
        # No need to explicitly close the connection; SQLAlchemy manages that
        print("Connection check completed")