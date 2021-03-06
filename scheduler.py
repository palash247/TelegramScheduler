from datetime import datetime, timedelta
import sys
import os
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

logger = logging.getLogger('schedules')

scheduler = BackgroundScheduler()
url = 'sqlite:////home/palash/surveyor.db'
scheduler.add_jobstore('sqlalchemy', url=url)
try:
    scheduler.start()
    logger.info('Scheduler started successfully.')
except (KeyboardInterrupt, SystemExit):
    pass
