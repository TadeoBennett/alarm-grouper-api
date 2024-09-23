from db import db

from datetime import datetime

class UserCategoryModel(db.Model):
    __tablename__ = "user_categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name
        self.created_at = str(datetime.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self, name, description, color):
        self.name = name
        self.description = description
        self.color = color
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "created_at": self.created_at
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_userid_and_name(cls, user_id, name):
        return cls.query.filter_by(user_id=user_id, name=name).first()

