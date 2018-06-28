from db import db

class MessageModel(db.Model):

    __tablename__ = "messages"

    _id = db.Column('id', db.VARCHAR(119), primary_key=True)
    name = db.Column('name', db.String())
    text = db.Column('text', db.String())
    schedule = db.Column('schedule', db.String())
    chat_id = db.Column(
        'chat_id',
        db.Integer,
        db.ForeignKey('groups.chat_id')
    )
    group = db.relationship('GroupModel')

    def __init__(self, _id, name, text, schedule, chat_id):
        self.id = _id
        self.name = name
        self.text = text
        self.schedule = schedule
        self.chat_id = chat_id

    def json(self):
        return {'id':self.id, 'name': self.name, 'text': self.text, 'schedule': self.schedule}

    @classmethod
    def find_by_name_and_chat_id(cls, name, chat_id):
        return cls.query.filter_by(name=name, chat_id=chat_id).first()

    @classmethod
    def find_by_chat_id(cls, chat_id):
        return cls.query.filter_by(chat_id=chat_id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
