from django.db import models
from django.core.exceptions import ValidationError

class Image(models.Model):
    name = models.CharField("Название картинки", max_length=100, default="Без названия")
    url = models.URLField("URL изображения")

    def __str__(self):
        return self.name

class Banner(models.Model):
    title = models.CharField("Название баннера", max_length=100, default="Без названия")
    images = models.ManyToManyField(Image, related_name="banners", verbose_name="Изображения баннера")
    link = models.URLField("Ссылка на сайт", help_text="URL для перехода при нажатии")
    is_active = models.BooleanField("Активный", default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            Banner.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Баннер: {self.title}"

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
