from app import app
from db import db

@app.before_first_request
def create_table():
    import create_tables