import sqlite3

connection = sqlite3.connect('surveyor.db')
cursor = connection.cursor()

cursor.execute(
    'create table if not exists groups (id integer primary key, name text,chat_id integer, time_zone text)')

connection.commit()
connection.close()
