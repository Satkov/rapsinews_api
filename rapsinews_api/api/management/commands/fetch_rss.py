import feedparser
from django.core.management.base import BaseCommand
from api.models import Post
from dateutil import parser as dateparser
from bs4 import BeautifulSoup
import html
import re
import logging

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

                post, created = Post.objects.update_or_create(
                    link=link,
                    defaults={
                        'title': entry.get('title', 'Без заголовка'),
                        'category': entry.get('category', 'Без категории'),
                        'published': published,
                        'full_text': clean_text,
                        'image': image_url,
                    }
                )

                if created:
                    logger.info(f'Добавлено: {post.title}')
                else:
                    logger.info(f'Обновлено: {post.title}')

            except Exception as e:
                logger.error(f'Ошибка обработки записи: {e}')

    @staticmethod
    def remove_news_prefix(text):
        # Удаляет префикс "МОСКВА, 17 апр — РАПСИ."
        pattern = r'^МОСКВА,\s\d{1,2}\s[а-я]+\s—\sРАПСИ\.\s*'
        return re.sub(pattern, '', text, flags=re.IGNORECASE)
