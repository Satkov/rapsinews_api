import feedparser
from django.core.management.base import BaseCommand
from api.models import Post
from dateutil import parser as dateparser
from bs4 import BeautifulSoup
import html
import re
import logging
from django.db import transaction


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Парсит RSS-ленту и сохраняет (или обновляет) записи в БД'

    def handle(self, *args, **options):
        feed_url = 'https://rapsinews.ru/export/yandex/rss2/index.xml'
        try:
            feed = feedparser.parse(feed_url)
            logger.info(f'Получено {len(feed.entries)} записей из RSS.')
        except Exception as e:
            logger.error(f'Ошибка при парсинге RSS: {e}')
            return

        added_count = 0
        updated_count = 0

        bulk_create = []
        bulk_update = []

        for entry in feed.entries:
            try:
                required_fields = ['link', 'title', 'category', 'published', 'yandex_full-text']

                missing_fields = [field for field in required_fields if not entry.get(field)]
                if missing_fields:
                    logger.warning(f"Запись пропущена: отсутствуют поля {', '.join(missing_fields)}")
                    continue

                link = entry.get('link')

                html_raw = entry.get('yandex_full-text', '')
                soup = BeautifulSoup(html_raw, 'html.parser')
                clean_text = soup.get_text(separator='\n')
                clean_text = html.unescape(clean_text)
                clean_text = self.remove_news_prefix(clean_text)

                image_url = None
                if 'enclosures' in entry and entry.enclosures:
                    image_url = entry.enclosures[0].get('href')

                try:
                    published = dateparser.parse(entry.get('published', '1970-01-01'))
                except Exception as e:
                    logger.warning(f'Ошибка разбора даты: {e}, используется значение по умолчанию.')
                    published = dateparser.parse('1970-01-01')

                existing_post = Post.objects.filter(link=link).first()
                if existing_post:
                    if (existing_post.title == entry.get('title')
                        and existing_post.category == entry.get('category')
                        and existing_post.published == published
                        and existing_post.full_text == clean_text):
                        continue

                    existing_post.title = entry.get('title', 'Без заголовка')
                    existing_post.category = entry.get('category', 'Без категории')
                    existing_post.published = published
                    existing_post.full_text = clean_text
                    existing_post.image = image_url
                    bulk_update.append(existing_post)
                    updated_count += 1
                else:
                    bulk_create.append(Post(
                        link=link,
                        title=entry.get('title', 'Без заголовка'),
                        category=entry.get('category', 'Без категории'),
                        published=published,
                        full_text=clean_text,
                        image=image_url,
                    ))
                    added_count += 1

            except Exception as e:
                logger.error(f'Ошибка обработки записи: {e}')

        with transaction.atomic():
            if bulk_create:
                Post.objects.bulk_create(bulk_create)
            if bulk_update:
                Post.objects.bulk_update(bulk_update, ['title', 'category', 'published', 'full_text', 'image'])

        logger.info(f'Обновлено: {updated_count} новостей, Добавлено: {added_count} новостей')

    @staticmethod
    def remove_news_prefix(text):
        pattern = r'^МОСКВА,\s\d{1,2}\s[а-я]+\s—\sРАПСИ\.\s*'
        return re.sub(pattern, '', text, flags=re.IGNORECASE)
