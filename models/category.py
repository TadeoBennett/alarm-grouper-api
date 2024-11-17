from db import db
from datetime import datetime


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category_creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    
    category_creator = db.relationship("UserModel", backref="categories")
    group = db.relationship("GroupModel", backref="categories")
    

    def __init__(self, category_creator_id, group_id, name, description, created_at):
        self.category_creator_id = category_creator_id
        self.group_id = group_id
        self.name = name        
        self.description = description
        self.created_at = created_at

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            print("Category created in database for user id: ", self.category_creator_id)
        except Exception as e:
            db.session.rollback()
            print(f"Error committing to the database: {e}")
            raise Exception("Error committing to the database")

    def json(self):
        return {
            "id": self.id,
            "category_creator_id": self.category_creator_id,
            "group_id": self.group_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at
        }

    @classmethod
    def get_all_categories(cls):
        return cls.query.all()

    @classmethod
    def get_category_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    # ---------------------- 
    @classmethod
    def get_category_by_id_and_user_id(cls, category_id, category_creator_id):
        return cls.query.filter_by(category_creator_id=category_creator_id, id=category_id).first()
    
    @classmethod
    def get_categories_by_user_id(cls, category_creator_id):
        return cls.query.filter_by(category_creator_id=category_creator_id).all()
    
    @classmethod
    def update_category_by_id_and_user_id(cls, category_creator_id, category_id, name, description):
        category = cls.query.filter_by(category_creator_id=category_creator_id, id=category_id).first()
        category.name = name
        category.description = description
        db.session.commit
    
    @classmethod
    def delete_category_by_id_and_user_id(cls, category_creator_id, category_id):
        category = cls.query.filter_by(category_creator_id=category_creator_id, id=category_id).first()
        db.session.delete(category)
        db.session.commit()
        print("Category deleted from database for user id: ", category_creator_id)

