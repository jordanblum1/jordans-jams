from jordansJams import getJams, notifyJordan
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone='US/Pacific')

mongo = MongoClient()
numbers = mongo.jordansJams.numbers


@sched.scheduled_job('cron', day_of_week='mon', hour=22, timezone="US/Pacific")
def notifyJ():
    notifyJordan()


    
sched.start()