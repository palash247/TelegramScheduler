# from datetime import datetime
# import time
# import os

# from apscheduler.schedulers.background import BackgroundScheduler


# def tick():
#     print('Tick! The time is: %s' % datetime.now())


# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(tick, 'interval', seconds=3)
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         scheduler.shutdown()


from datetime import datetime, timedelta
import sys
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler


def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    url = sys.argv[1] if len(sys.argv) > 1 else 'sqlite:///example.sqlite'
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
