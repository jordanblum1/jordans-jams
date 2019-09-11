from jordansJams import getJams
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

mongo = MongoClient()
numbers = mongo.jordansJams.numbers

#@sched.scheduled_job('cron', hour=10, timezone='US/Pacific')
def send_text():
    for number in numbers:
        getJams(numbers)
    


sched.start()