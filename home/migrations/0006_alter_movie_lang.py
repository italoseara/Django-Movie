# Generated by Django 4.0 on 2021-12-26 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_movie_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='lang',
            field=models.CharField(choices=[('en', 'Inglês'), ('pt-br', 'Português')], max_length=255),
        ),
    ]
