# Generated by Django 5.1 on 2025-05-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL изображения')),
            ],
        ),
        migrations.RemoveField(
            model_name='banner',
            name='images',
        ),
        migrations.AddField(
            model_name='banner',
            name='images',
            field=models.ManyToManyField(related_name='banners', to='banners.image', verbose_name='Изображения баннера'),
        ),
    ]
