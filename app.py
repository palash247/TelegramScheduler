from flask import Flask
from flask_restful import Api
from resourcess.update import Update
import os
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

TOKEN = os.environ.get('TELEGRAM_TOKEN')

app = Flask(__name__)
app.secret_key = 'palash'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surveyor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
import auth
app.register_blueprint(auth.bp)
import dashboard
app.register_blueprint(dashboard.bp)

api = Api(app)

@app.before_first_request
def create_table():
    import sqlite3
    connection = sqlite3.connect('surveyor.db')
    cursor = connection.cursor()
    groups_table = 'create table if not exists groups (id integer primary key autoincrement, name text,chat_id integer, time_zone text, unique(chat_id))'
    messages_table = 'create table if not exists messages (id varchar(191) primary key, name text, chat_id integer, "text" text, schedule text, foreign key(chat_id) references groups(id))'
    apscheduler_jobs_table = 'CREATE TABLE if not exists apscheduler_jobs(id VARCHAR(191) NOT NULL,next_run_time FLOAT,job_state BLOB NOT NULL,PRIMARY KEY(id))'
    user = 'create table if not exists user(id integer primary key autoincrement, username text unique not null, password not null)'
    delete_trigger = 'create trigger if not exists after delete on apscheduler_jobs BEGIN delete from messages where id=old.id; END;'
    cursor.execute(groups_table)
    cursor.execute(messages_table)
    cursor.execute(apscheduler_jobs_table)
    cursor.execute(user)
    cursor.execute(delete_trigger)

    connection.commit()
    connection.close()



api.add_resource(Update, '/{}'.format(TOKEN))


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000)
