# Generated by Django 5.1 on 2025-05-15 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_image_remove_banner_images_banner_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активный'),
        ),
        migrations.AddField(
            model_name='banner',
            name='title',
            field=models.CharField(default='Без названия', max_length=100, verbose_name='Название баннера'),
        ),
    ]
