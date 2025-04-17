from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        func=call_command,
        args=["fetch_rss"],
        trigger="interval",
        minutes=5,
        id="fetch_rss_job",
        name="Автозапуск fetch_rss каждые 5 минут",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Планировщик задач запущен.")