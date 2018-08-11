from db import db


class GroupModel(db.Model):
    __tablename__ = 'groups'
    

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(80))
    chat_id = db.Column('chat_id', db.Integer, unique=True)
    time_zone = db.Column('time_zone', db.String(80))
    messages = db.relationship('MessageModel', lazy='dynamic')

    def __init__(self, name, chat_id, time_zone):
        self.name = name
        self.chat_id = chat_id
        self.time_zone = time_zone

    def json(self):
        return {
            'name': self.name,
            'chat_id': self.chat_id,
            'time_zone': self.time_zone,
            'messages': list(map(lambda x: x.json(), self.messages.all()))
        }

    @classmethod
    def find_by_chat_id(cls, chat_id):
        return cls.query.filter_by(chat_id=chat_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
