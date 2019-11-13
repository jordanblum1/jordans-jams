from jordansJams import getJams, notifyJordan
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone='US/Pacific')

mongo = MongoClient()
numbers = mongo.jordansJams.numbers


@sched.scheduled_job('cron', day_of_week='tue', hour=21, minute=59, timezone="US/Pacific")
def notifyJ():
    print("it fired off the notification")
    notifyJordan()

sched.start()