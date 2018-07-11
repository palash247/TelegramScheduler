from app import app
from db import db

db.init_app(app)


@app.before_first_request
def create_table():

    db.create_all()
    db.session.execute(
        'create trigger if not exists after delete on apscheduler_jobs BEGIN delete from messages where id=old.id; END;')
    db.session.execute(
        'create table if not exists user(id integer primary key autoincrement, username text unique not null, password not null)')
    import auth
    app.register_blueprint(auth.bp)
    import dashboard
    app.register_blueprint(dashboard.bp)
    db.session.commit()
    db.session.close()



