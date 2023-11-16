from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .tasks import send_weekly_email_notifications


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        send_weekly_email_notifications,
        trigger="interval",
        weeks=1,
        day_of_week='sat',  # Specify the day of the week for the emails
        hour=7,  # Specify the hour for the emails (24-hour format)
        minute=18,  # Specify the minute for the emails
    )

    scheduler.start()
    print("Scheduler started!")