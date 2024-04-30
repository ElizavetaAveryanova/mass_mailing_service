from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from newapp.utils import print_time_job


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        print_time_job,
        trigger=IntervalTrigger(minutes=1),
        id="print_time_second",  # Уникальный ID для задачи
        max_instances=1,
        replace_existing=True
    )

    scheduler.start()