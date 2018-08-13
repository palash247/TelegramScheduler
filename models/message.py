from db import db

class MessageModel(db.Model):

    __tablename__ = "messages"

    id = db.Column('id', db.String(119),primary_key=True)
    name = db.Column('name', db.String())
    message = db.Column('message', db.String())
    schedule = db.Column('schedule', db.String())
    group_id = db.Column(
        'group_id',
        db.Integer,
        db.ForeignKey('groups.id')
    )
    group = db.relationship('GroupModel')
    
    def __init__(self, id, name, message, schedule, group_id):
        self.id = id
        self.name = name
        self.message = message
        self.schedule = schedule
        self.group_id = group_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'message': self.message, 'schedule': self.schedule, 'group_id': self.group_id }

    @classmethod
    def find_by_name_and_group_id(cls, name, group_id):
        return cls.query.filter_by(name=name, group_id=group_id).first()

    @classmethod
    def find_by_chat_id(cls, group_id):
        return cls.query.filter_by(group_id=group_id).all()

    @classmethod
    def find_by_id(cls, group_id, _id):
        return cls.query.filter_by(id=_id, group_id=group_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
