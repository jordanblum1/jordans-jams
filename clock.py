from jordansJams import getJams, notifyJordan
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone='US/Pacific')

@sched.scheduled_job('cron', day_of_week='tue', hour=22 minute=5, timezone="US/Pacific")
def notifyJ():
    print("it fired off the notification")
    notifyJordan()

sched.start()