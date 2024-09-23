from datetime import datetime
from db import db
from passlib.hash import pbkdf2_sha256  #for hashing the password

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.created_at = str(datetime.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print("User created successfully")

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self, username, email):
        self.username = username
        self.email = email
        db.session.commit()

    def change_password(self, password):
        self.password = password
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # NOTE: verify password with hashed password in db
    @classmethod
    def find_by_email_and_password(cls, email, password):
        return cls.query.filter_by(email=email, password=password).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
    