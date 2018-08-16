from db import db


class GroupModel(db.Model):
    __tablename__ = 'groups'
    

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    channel_name = db.Column('channel_name', db.String())
    group_identifier = db.Column('group_identifier', db.String())
    messages = db.relationship('MessageModel', lazy='dynamic')
    whatsapp_groups = db.relationship('WhatsAppModel', lazy='dynamic')
    telegram_groups = db.relationship('TelegramModel',lazy='dynamic')

    def __init__(self, channel_name, group_identifier):
        self.channel_name = channel_name
        self.group_identifier = group_identifier

    def init_channel(self):
        if self.channel_name == 'whatsapp':
            whatsapp_group = self.whatsapp_groups.first()
            if whatsapp_group:
                self.channel = whatsapp_group
        if self.channel_name == 'telegram':
            telegram_group = self.telegram_groups.first()
            if telegram_group:
                self.channel = telegram_group
        
    def json(self):
        self.init_channel()
        print(self.channel_name, self.group_identifier)
        return {
            'channel': self.channel.json(),
            'messages': list(map(lambda x: x.json(), self.messages.all()))
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
