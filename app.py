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


api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Update, '/{}'.format(TOKEN))


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    import auth
    app.register_blueprint(auth.bp)
    import dashboard
    app.register_blueprint(dashboard.bp)
    app.run(port=5000)
