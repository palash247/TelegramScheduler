from datetime import datetime, timedelta
import sys
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler


def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    url = sys.argv[1] if len(sys.argv) > 1 else 'sqlite:///surveyor.db'
    scheduler.add_jobstore('sqlalchemy', url=url)
    alarm_time = datetime.now() + timedelta(seconds=2)
    scheduler.add_job(alarm, 'date', run_date=alarm_time,
                      args=[datetime.now()])
    print('To clear the alarms, delete the example.sqlite file.')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
        print('after scheduler starts')
        time.sleep(5)
        print('adding another alarm')
        scheduler.add_job(
            alarm, 'date', run_date=alarm_time + timedelta(seconds=5), args=[datetime.now()])
        print('another alarm added successfully')
        while 1:
            pass
    except (KeyboardInterrupt, SystemExit):
        pass
