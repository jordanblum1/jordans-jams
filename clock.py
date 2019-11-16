from jordansJams import getJams, notifyJordan
from apscheduler.schedulers.blocking import BlockingScheduler


def notifyJ():
    print("Jordan has been notified")
    notifyJordan()


sched = BlockingScheduler(timezone='US/Pacific')

sched.add_job(notifyJ, 'cron', day_of_week='fri', hour=18, minute=10, timezone="US/Pacific")

sched.start()