import sqlite3

connection = sqlite3.connect('surveyor.db')
cursor = connection.cursor()

whatsapp_table = 'create table if not exists whatsapp (group_name text primary key, group_fk integer, foreign key(group_fk) references groups(id))'
telegram_table = 'create table if not exists telegram (group_chat_id text primary key, group_name text, group_fk integer, foreign key(group_fk) references groups(id))'
groups_table = 'create table if not exists groups (id integer primary key autoincrement, channel_name text, group_identifier text)'
messages_table = 'create table if not exists messages (id varchar(191) primary key, name text, group_id integer, message text, schedule text, foreign key(group_id) references groups(id))'
apscheduler_jobs_table = 'CREATE TABLE apscheduler_jobs(id VARCHAR(191) NOT NULL,next_run_time FLOAT,job_state BLOB NOT NULL,PRIMARY KEY(id))'
user = 'create table if not exists user(id integer primary key autoincrement, username text unique not null, password not null)'
delete_trigger_message = 'create trigger if not exists after delete on apscheduler_jobs BEGIN delete from messages where id=old.id; END;'
delete_trigger_telegram = 'create trigger if not exists after delete on groups BEGIN delete from telegram where group_fk = old.id; END;'
delete_trigger_whatsapp = 'create trigger if not exists after delete on groups BEGIN delete from whatsapp where group_fk = old.id; END;'

cursor.execute(groups_table)
cursor.execute(messages_table)
cursor.execute(apscheduler_jobs_table)
cursor.execute(user)
cursor.execute(delete_trigger_message)
cursor.execute(whatsapp_table)
cursor.execute(telegram_table)
cursor.execute(delete_trigger_telegram)
cursor.execute(delete_trigger_whatsapp)


connection.commit()
connection.close()
