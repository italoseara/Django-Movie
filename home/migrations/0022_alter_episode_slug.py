# Generated by Django 4.0 on 2021-12-29 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_episode_slug_alter_episode_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]
