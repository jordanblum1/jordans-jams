from jordansJams import notifyJordan, getJams
from apscheduler.schedulers.blocking import BlockingScheduler
from connect import Connect
import time

def notifyJ():
    notifyJordan()

def notifySubscribers():
    numbers = Connect.get_connection().jordansJams.numbers
    for number in numbers.find():
        sendTo = number['_id']
        getJams(sendTo)
        time.sleep(1)

    

sched = BlockingScheduler(timezone='US/Pacific')

sched.add_job(notifyJ, 'cron', day_of_week='sun', hour=18, timezone="US/Pacific")

sched.add_job(notifySubscribers, 'cron', day_of_week='wed', hour=10, timezone="US/Pacific")

sched.start()