from django.apps import AppConfig
import os


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"

    def ready(self):
        from . import cache      # noqa: F401

        #    Планировщик запускаем только один раз,
        #    чтобы apscheduler не плодил дублирующих задач при autoreload
        if os.environ.get("RUN_MAIN") == "true":
            from rapsinews_api.api.management.commands import start_scheduler
            start_scheduler.start()
