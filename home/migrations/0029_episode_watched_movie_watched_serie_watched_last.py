# Generated by Django 4.0 on 2022-01-02 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_remove_episode_serie_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='watched',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='watched',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='serie',
            name='watched_last',
            field=models.IntegerField(default=1),
        ),
    ]