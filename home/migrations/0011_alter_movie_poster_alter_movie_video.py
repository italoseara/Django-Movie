# Generated by Django 4.0 on 2021-12-27 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_movie_poster_alter_movie_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(upload_to='<django.db.models.fields.SlugField>/poster/'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='video',
            field=models.FileField(upload_to='<django.db.models.fields.SlugField>/video/'),
        ),
    ]
