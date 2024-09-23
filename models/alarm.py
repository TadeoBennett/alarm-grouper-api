from db import db
from datetime import datetime


class AlarmModel(db.Model):
    __tablename__ = "alarms"

    id = db.Column(db.Integer, primary_key=True)
    creator_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("user_categories.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    ringTime = db.Column(db.String(50), nullable=False)
    ringDate = db.Column(db.String(50), nullable=False)
    repeat = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.String(50), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.created_at = str(datetime.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self, name, description, color, ring_time, ring_date, repeat, active):
        self.name = name
        self.description = description
        self.color = color
        self.ringTime = ring_time
        self.ringDate = ring_date
        self.repeat = repeat
        self.active = active
        db.session.commit()

    @classmethod
    def find_by_userid_and_name(cls, user_id, name):
        return cls.query.filter_by(creator_user_id=user_id, name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def json(self):
        return {
            "id": self.id,
            "creator_user_id": self.creator_user_id,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "ring_time": self.ringTime,
            "ring_date": self.ringDate,
            "repeat": self.repeat,
            "active": self.active,
            "created_at": self.created_at
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def find_active_alarms(cls):
        return cls.query.filter_by(active=True)

    @classmethod
    def find_repeat_alarms(cls):
        return cls.query.filter_by(repeat=True)

    @classmethod
    def find_alarms_by_category_id(cls, category_id):
        return cls.query.filter_by(category_id=category_id)