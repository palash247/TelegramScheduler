from db import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String, unique=True, nullable=False)
    password = db.Column('password', db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def json(self):
        return {'username': self.username}

    def verify(self):
        user = cls.query.filter_by.
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).fetchone()

    @classmethod
    def find_by_username_pass(cls, username, password):
        return cls.query.filter_by(username=username, password=password).fetchone()

    
