# Generated by Django 4.0 on 2021-12-29 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_episode_serie_episodes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='serie_slug',
        ),
        migrations.AlterField(
            model_name='episode',
            name='file',
            field=models.FileField(upload_to='./'),
        ),
    ]