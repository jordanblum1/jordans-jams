from jordansJams import notifyJordan
from apscheduler.schedulers.blocking import BlockingScheduler


def notifyJ():
    notifyJordan()

sched = BlockingScheduler(timezone='US/Pacific')

sched.add_job(notifyJ, 'cron', day_of_week='fri', hour=19, timezone="US/Pacific")

sched.start()