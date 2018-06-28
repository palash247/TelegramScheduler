from datetime import datetime, timedelta
import sys
import os
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO, filename='log/schedules.log')

logger = logging.getLogger()

scheduler = BackgroundScheduler()
url = 'sqlite:///surveyor.db'
scheduler.add_jobstore('sqlalchemy', url=url)
try:
    scheduler.start()
    logger.info('Scheduler started successfully.')
except (KeyboardInterrupt, SystemExit):
    pass