import feedparser
from django.core.management.base import BaseCommand
from api.models import Post
from dateutil import parser as dateparser
from bs4 import BeautifulSoup
import html

class Command(BaseCommand):
    help = 'Парсит RSS-ленту и сохраняет (или обновляет) записи в БД'

    def handle(self, *args, **options):
        feed_url = 'https://rapsinews.ru/export/yandex/rss2/index.xml'
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            html_raw = entry.get('yandex_full-text', '') or entry.get('summary', '')
            soup = BeautifulSoup(html_raw, 'html.parser')
            clean_text = soup.get_text(separator='\n')
            clean_text = html.unescape(clean_text)

            post, created = Post.objects.update_or_create(
                link=entry.get('link'),
                defaults={
                    'title': entry.get('title', 'Без заголовка'),
                    'category': entry.get('category', 'Без категории'),
                    'published': dateparser.parse(entry.get('published', '1970-01-01')),
                    'full_text': clean_text,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Добавлено: {post.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Обновлено: {post.title}'))