# Generated by Django 4.0 on 2021-12-29 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_serie_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie_slug', models.SlugField(max_length=255, unique=True)),
                ('file', models.FileField(upload_to='<django.db.models.fields.SlugField>/')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='serie',
            name='episodes',
            field=models.ManyToManyField(to='home.Episode'),
        ),
    ]
