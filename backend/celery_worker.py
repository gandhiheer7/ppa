from app import create_app
from extensions import celery_app
from celery.schedules import crontab
import tasks # Import tasks to register them

app = create_app()
app.app_context().push()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Runs daily at 8:00 AM [cite: 115]
    sender.add_periodic_task(
        crontab(hour=8, minute=0),
        tasks.daily_deadline_reminders.s(),
        name='Send daily application reminders'
    )

    # Runs on the 1st day of every month at 9:00 AM [cite: 121]
    sender.add_periodic_task(
        crontab(day_of_month='1', hour=9, minute=0),
        tasks.monthly_activity_report.s(),
        name='Send monthly admin activity report'
    )