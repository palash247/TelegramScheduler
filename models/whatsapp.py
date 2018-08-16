from db import db

class WhatsAppModel(db.Model):
    __tablename__ = 'whatsapp'

    group_name = db.Column('group_name', db.String(),primary_key=True)
    group_fk = db.Column('group_fk', db.Integer, db.ForeignKey('groups.id'))

    group = db.relationship('GroupModel')

    def __init__(self, group_name, group_fk):
        self.group_name = group_name
        self.group_fk = group_fk

    def json(self):
        return {
            'group_fk': self.group_fk,
            'channel_name': 'whatsapp',
            'group_name': self.group_name,
        }

    @classmethod
    def find_by_name(cls, group_name):
        return cls.query.filter_by(group_name=group_name).first()

    @classmethod
    def find_by_id(cls, group_fk):
        return cls.query.filter_by(group_fk=group_fk).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
