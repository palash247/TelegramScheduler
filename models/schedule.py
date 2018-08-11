
from db import db
from sqlalchemy.types import LargeBinary
from sqlalchemy import event


class ScheduleModel(db.Model):

    __tablename__ = "apscheduler_jobs"
    id = db.Column('id', db.String(191), primary_key=True, nullable=False)
    next_run_time = db.Column('next_run_time', db.Float, nullable=False)
    job_state = db.Column('job_state', db.LargeBinary, nullable=False)

