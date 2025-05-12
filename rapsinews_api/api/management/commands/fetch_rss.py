import feedparser
import html
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from dateutil import parser as dateparser
from api.models import Post
from datetime import datetime


class Command(BaseCommand):
    help = 'Парсит RSS-ленту и сохраняет (или обновляет) записи в БД через bulk'

    def handle(self, *args, **options):
        feed_url = 'https://rapsinews.ru/export/yandex/rss2/index.xml'
        feed = feedparser.parse(feed_url)

        entries = feed.entries

        existing_posts = Post.objects.in_bulk(field_name='link')
        existing_links = set(existing_posts.keys())

        to_create = []
        to_update = []

        for entry in entries:
            link = entry.get('link')
            if not link:
                continue

            html_raw = entry.get('yandex_full-text', '')
            soup = BeautifulSoup(html_raw, 'html.parser')
            clean_text = soup.get_text(separator='\n')
            clean_text = html.unescape(clean_text)
            clean_text = self.remove_news_prefix(clean_text)

            # картинка
            image_url = None
            if 'enclosures' in entry and entry.enclosures:
                image_url = entry.enclosures[0].get('href')

            post_data = {
                'title': entry.get('title', 'Без заголовка'),
                'link': link,
                'category': entry.get('category', 'Без категории'),
                'published': dateparser.parse(entry.get('published', datetime.now())),
                'full_text': clean_text,
                'image': image_url,
            }

            if link in existing_links:
                # обновляем только посты, в которых есть изменения
                # создаем только посты, которых нет в базе
                post = existing_posts[link]
                updated = False
                for field, value in post_data.items():
                    if getattr(post, field) != value:
                        setattr(post, field, value)
                        updated = True
                if updated:
                    to_update.append(post)
            else:
                to_create.append(Post(**post_data))

        if to_create:
            Post.objects.bulk_create(to_create)

        if to_update:
            Post.objects.bulk_update(to_update, ['title', 'category', 'published', 'full_text', 'image'])

        self.stdout.write(self.style.SUCCESS(f'Обновленно в: {datetime.now()}'))
        self.stdout.write(self.style.SUCCESS(f'Добавлено: {len(to_create)} записей'))
        self.stdout.write(self.style.SUCCESS(f'Обновлено: {len(to_update)} записей'))

    @staticmethod
    def remove_news_prefix(text):
        pattern = r'^МОСКВА,\s\d{1,2}\s[а-я]+\s—\sРАПСИ\.\s*'
        return re.sub(pattern, '', text, flags=re.IGNORECASE)