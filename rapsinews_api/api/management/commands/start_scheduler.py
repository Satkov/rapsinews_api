from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command
import logging, time

logger = logging.getLogger(__name__)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        func=call_command,
        args=["fetch_rss"],
        trigger="interval",
        seconds=300,
        id="fetch_rss_job",
        name="Парсинг RSS каждые 300 секунд",
        replace_existing=True,
    )

    try:
        scheduler.start()
        logger.info("Планировщик задач успешно запущен.")
        while True:
            time.sleep(60)
    except Exception as e:
        logger.error(f"Ошибка запуска планировщика: {e}")


class Command(BaseCommand):
    help = 'Запуск фонового планировщика'

    def handle(self, *args, **kwargs):
        start_scheduler()
        self.stdout.write(self.style.SUCCESS("Планировщик запущен."))
