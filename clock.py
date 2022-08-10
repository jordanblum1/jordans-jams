'''importing time, connect, and scheduler to run the jams'''
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from connect import Connect
from jordansJams import notify_jordan, get_jams

def notifyj():
    '''sends notification to jordan to send in jams'''
    notify_jordan()

def notify_subscribers():
    '''sends out the jams @ 10am PST to subs'''
    numbers = Connect.get_connection().jordansJams.numbers
    for number in numbers.find():
        send_to = number['_id']
        get_jams(send_to)
        time.sleep(1)


sched = BlockingScheduler(timezone='US/Pacific')

sched.add_job(notifyj, 'cron', day_of_week='sun', hour=18, timezone="US/Pacific")

sched.add_job(notify_subscribers, 'cron', day_of_week='wed', hour=10, timezone="US/Pacific")

sched.start()
