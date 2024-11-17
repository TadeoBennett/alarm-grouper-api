from db import db
from datetime import datetime



class SoundModel(db.Model):
    __tablename__ = "sounds"
    
    id = db.Column(db.Integer, primary_key=True)
    sound_creator_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    file = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, sound_creator_id, name, file, description, created_at = None):
        self.sound_creator_id = sound_creator_id
        self.name = name
        self.file = file
        self.description = description
        self.created_at = str(datetime.now())
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print("Sound created in database")
        
    def json(self):
        return {
            "id": self.id,
            "creator_id": "System" if (self.sound_creator_id == 1) else self.sound_creator_id,
            "name": self.name,
            "file": self.file,
            "description": self.description,
            "created_at": self.created_at
        }
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        print("Sound deleted from database with id: ", self.id)
        
    @classmethod
    def get_all_sounds(cls):
        return cls.query.all()
    
    @classmethod
    def get_sound_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def get_sounds_by_user_id(cls, user_id):
        return cls.query.filter_by(sound_creator_id=user_id).all()
    
    @classmethod
    def get_sound_by_id_and_user_id(cls, sound_id, user_id):
        return cls.query.filter_by(id=sound_id, sound_creator_id=user_id).first()
    # @classmethod
    # def delete_sound_by_id(cls, _id):
    #     sound = cls.query.filter_by(id=_id).first()
    #     db.session.delete(s)
    #     db.session.commit()
    #     print("Sound deleted with id: ", _id)