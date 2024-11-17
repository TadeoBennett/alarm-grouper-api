from db import db
from datetime import datetime
from models import CategoryModel
from models import AlarmModel


class GroupModel(db.Model):
    __tablename__ = "groups"
    
    id = db.Column(db.Integer, primary_key=True)
    group_creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    group_creator = db.relationship("UserModel", backref="groups")
    
    def __init__(self, group_creator_id, name, description):
        self.group_creator_id = group_creator_id
        self.name = name
        self.description = description
        self.created_at = str(datetime.now())
    
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print("Group created in database for user id: ", self.group_creator_id)
    
    def json(self):
        return {
            "id": self.id,
            "group_creator_id": self.group_creator_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at
        }
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        print("Group deleted from database with id: ", self.id)
    
    @classmethod
    def get_groups_by_user_id(cls, group_creator_id):
        return cls.query.filter_by(group_creator_id=group_creator_id).all() 
    
    @classmethod
    def get_nested_group_data_by_user_id(cls, user_id):
        groups = [group.json() for group in GroupModel.get_groups_by_user_id(user_id)]
        alarms = [alarm.json() for alarm in AlarmModel.get_alarms_by_user_id(user_id)]
        categories = [category.json() for category in CategoryModel.get_categories_by_user_id(user_id)]
        # editing addtiional details of the values --------------
        for group in groups:
            # count the numnber of catgeories in the group
            group["categories_count"] = len([category for category in categories if category["group_id"] == group["id"]])

        for category in categories:
            # count the numnber of alarms in the category
            category["alarms_count"] = len([alarm for alarm in alarms if alarm["category_id"] == category["id"]])
        
        # -------------------------------------------------------
        
        # print("Groups: ", groups)
        # print("Categories: ", categories)
        # print("Alarms: ", alarms)
        return {
            "quantities": {
                "groups": len(groups),
                "categories": len(categories),
                "alarms": len(alarms)
            },
            "groups": groups,
            "categories": categories,
            "alarms": alarms
        }
    
    @classmethod
    def get_group_by_id(cls, group_id):
        return cls.query.filter_by(id=group_id).first()
    
    @classmethod
    def get_group_by_id_and_user_id(cls, group_id, group_creator_id):
        return cls.query.filter_by(group_creator_id=group_creator_id, id=group_id).first()
    
    @classmethod
    def update_group_by_id_and_user_id(cls, group_creator_id, group_id, name, description):
        group = cls.query.filter_by(group_creator_id=group_creator_id, id=group_id).first()
        group.name = name
        group.description = description
        db.session.commit()
        print("Group updated with id: ", group_id)
    
    @classmethod
    def delete_group_by_id_and_user_id(cls, group_creator_id, group_id):
        group = cls.query.filter_by(group_creator_id=group_creator_id, id=group_id).first()
        db.session.delete(group)
        db.session.commit()
        print("Group deleted with id: ", group_id)