# Generated by Django 4.0 on 2021-12-31 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_rename_title_episode_serie_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='serie_title',
        ),
    ]