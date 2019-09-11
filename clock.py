from jordansJams import getJams
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=10, timezone='US/Pacific')
def send_text():
    ()


sched.start()