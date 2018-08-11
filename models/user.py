from db import db

class UserModel(db.Model):

    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String, unique=True)
    password = db.Column('password', db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def json(self):
        return {"user_id":self.id, 'username': self.username}

    @classmethod
    def is_available(cls, username):
        return cls.query.filter_by(username=username).first()
        

    def create_user(self):
        if not UserModel.is_available(self.username):
            db.session.add(self)
            db.session.commit()
            return True
        return False

    def remove_user(self):
        if not UserModel.is_available(self.username):
            db.session.remove(self)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        

    @classmethod
    def validate_user(cls, username, password):
        return cls.query.filter_by(username=username, password=password).first()

    
