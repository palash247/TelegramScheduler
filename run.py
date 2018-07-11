from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_table():

    db.create_all()
    db.session.execute(
        'create trigger if not exists after delete on apscheduler_jobs BEGIN delete from messages where id=old.id; END;')
    db.session.commit()
    db.session.close()


