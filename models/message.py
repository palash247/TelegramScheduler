from db import db


class MessageModel(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    text = db.Column(db.String(500))
    schedule = db.Column(db.Float)

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship('GroupModel')

    def __init__(self, name, text, schedule, group_id):
        self.name = name
        self.text = text
        self.schedule = schedule
        self.group_id = group_id

    def json(self):
        return {'name': self.name, 'text': self.text, 'schedule': self.schedule}

    @classmethod
    def find_by_name(cls, name, group_id):
        return cls.query.filter_by(name=name, group_id=group_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
