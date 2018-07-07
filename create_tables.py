import sqlite3

connection = sqlite3.connect('surveyor.db')
cursor = connection.cursor()
groups_table = 'create table if not exists groups (id integer primary key autoincrement, name text,chat_id integer, time_zone text, unique(chat_id))'
messages_table = 'create table if not exists messages (id varchar(191) primary key, name text, chat_id integer, "text" text, schedule text, foreign key(chat_id) references groups(id))'
apscheduler_jobs_table = 'CREATE TABLE apscheduler_jobs(id VARCHAR(191) NOT NULL,next_run_time FLOAT,job_state BLOB NOT NULL,PRIMARY KEY(id))'
user = 'create table if not exists user(id integer primary key autoincrement, username text unique not null, password not null)'
delete_trigger = 'create trigger if not exists after delete on apscheduler_jobs BEGIN delete from messages where id=old.id; END;'
cursor.execute(groups_table)
cursor.execute(messages_table)
cursor.execute(apscheduler_jobs_table)
cursor.execute(user)
cursor.execute(delete_trigger)

connection.commit()
connection.close()
