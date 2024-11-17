from db import db
from datetime import datetime
from sqlalchemy import Time, Date



class AlarmModel(db.Model):
    __tablename__ = "alarms"

    id = db.Column(db.Integer, primary_key=True)
    alarm_creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ringTime = db.Column(Time, nullable=True)
    ringDate = db.Column(Date, nullable=True)
    repeat = db.Column(db.Boolean, nullable=False)
    sound_id = db.Column(db.Integer, db.ForeignKey("sounds.id"), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    category = db.relationship("CategoryModel", backref="alarms")
    alarm_creator = db.relationship("UserModel", backref="alarms")
    sound = db.relationship("SoundModel", backref="alarms")
    

    def __init__(self, alarm_creator_id, category_id, name, description, ringTime, ringDate, repeat, sound_id, active, created_at):
        self.alarm_creator_id = alarm_creator_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.ringTime = ringTime
        self.ringDate = ringDate
        self.repeat = repeat
        self.sound_id = sound_id
        self.active = active
        self.created_at = created_at

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print("Alarm created in database for user id: ", self.alarm_creator_id)

    def json(self):
        return {
            "id": self.id,
            "alarm_creator_id": self.alarm_creator_id,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "ringTime": self.ringTime.strftime('%H:%M'),
            "ringDate": self.ringDate.strftime('%Y-%m-%d'),
            "repeat": self.repeat,
            "active": self.active,
            "sound_id": self.sound_id,
            "created_at": self.created_at
        }
        
    @classmethod
    def get_alarm_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def get_alarms_by_user_id(cls, alarm_creator_id):
        return cls.query.filter_by(alarm_creator_id=alarm_creator_id).all()
    
    @classmethod
    def get_alarm_by_id_and_user_id(cls, alarm_id, alarm_creator_id):
        return cls.query.filter_by(alarm_creator_id=alarm_creator_id, id=alarm_id).first()
    
    @classmethod
    def update_alarm_by_id_and_user_id(cls, alarm_creator_id, alarm_id, name, description):
        alarm = cls.query.filter_by(alarm_creator_id=alarm_creator_id, id=alarm_id).first()
        alarm.name = name
        alarm.description = description
        db.session.commit()
        
    @classmethod
    def delete_alarm_by_id_and_user_id(cls, alarm_creator_id, alarm_id):
        alarm = cls.query.filter_by(alarm_creator_id=alarm_creator_id, id=alarm_id).first()
        db.session.delete(alarm)
        db.session.commit()