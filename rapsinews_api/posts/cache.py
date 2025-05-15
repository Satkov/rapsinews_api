from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post


PREFIX = "post_list:"
TTL    = 300


def key_for(request):
    """Строим ключ из полного URL — limit/offset уже включены."""
    return f"{PREFIX}{request.get_full_path()}"


@receiver([post_save, post_delete], sender=Post)
def invalidate_post_list_cache(**kwargs):
    """Сбиваем ВСЕ варианты списка сразу после изменения модели."""
    cache.delete_pattern(f"{PREFIX}*")
