from django.core.management.base import BaseCommand
from api.models import Post

class Command(BaseCommand):
    help = 'Удаляет все записи из модели Post'

    def handle(self, *args, **options):
        count, _ = Post.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {count} записей из Post'))