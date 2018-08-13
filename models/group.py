from db import db


class GroupModel(db.Model):
    __tablename__ = 'groups'
    

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    channel_name = db.Column('channel_name', db.String())
    group_identifier = db.Column('group_identifier', db.String())
    messages = db.relationship('MessageModel', lazy='dynamic')
    whatsapp = db.relationship('WhatsAppModel', lazy='dynamic')
    telegram = db.relationship('TelegramModel',lazy='dynamic')

    def __init__(self, channel_name, group_identifier):
        self.channel_name = channel_name
        self.group_identifier = group_identifier

    def json(self):
        return {
            'channel': self.whatsapp.json() if self.channel_name=='whatsapp' else self.telegram.json(),
            'messages': list(map(lambda x: x.json(), self.messages.all()))
        }

    @classmethod
    def find_by_group_identifier(cls, group_identifier):
        return cls.query.filter_by(group_identifier=group_identifier).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
