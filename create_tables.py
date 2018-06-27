import sqlite3

connection = sqlite3.connect('surveyor.db')
cursor = connection.cursor()
groups_table = 'create table if not exists groups (id integer primary key autoincrement, name text,chat_id integer, time_zone text, unique(chat_id))'
messages_table = 'create table if not exists messages (id integer primary key autoincrement, name text, chat_id integer, "text" text, schedule integer, foreign key(chat_id) references groups(id))'
cursor.execute(groups_table)
cursor.execute(messages_table)

connection.commit()
connection.close()
