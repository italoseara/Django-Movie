# Generated by Django 4.0 on 2022-01-03 00:33

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_episode_watched_movie_watched_serie_watched_last'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='subtitles',
            field=models.FileField(blank=True, default=None, null=True, upload_to=home.models.get_file_path),
        ),
        migrations.AddField(
            model_name='movie',
            name='subtitles',
            field=models.FileField(blank=True, default=None, null=True, upload_to=home.models.get_file_path),
        ),
    ]