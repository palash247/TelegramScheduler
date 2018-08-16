from db import db


class TelegramModel(db.Model):
    __tablename__ = 'telegram'

    group_chat_id = db.Column('group_chat_id', db.String(), primary_key=True)
    group_name = db.Column('group_name', db.String())
    group_fk = db.Column('group_fk', db.Integer,
                         db.ForeignKey('groups.id'))

    group = db.relationship('GroupModel')

    def __init__(self, group_chat_id, group_name, group_fk):
        self.group_chat_id = group_chat_id
        self.group_name = group_name
        self.group_fk = group_fk
    
    def json(self):
        return {
            'group_fk': self.group_fk,
            'channel_name': 'telegram',
            'group_chat_id': self.group_chat_id,
            'group_name': self.group_name
        }

    @classmethod
    def find_by_name(cls, group_name):
        return cls.query.filter_by(group_name=group_name).first()

    @classmethod
    def find_by_group_chat_id(cls, group_chat_id):
        return cls.query.filter_by(group_chat_id=group_chat_id).first()
    
    @classmethod
    def find_by_id(cls, group_fk):
        return cls.query.filter_by(group_fk=group_fk).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
