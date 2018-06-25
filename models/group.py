from db import db


class GroupModel(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    chat_id = db.Column(db.Integer)
    time_zone = db.Column(db.String(80))

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
            'messages': [message.json() for message in self.messages.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
