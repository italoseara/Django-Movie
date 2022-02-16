import os
import cv2
from pathlib import Path
from datetime import timedelta
from mimetypes import guess_type

from django.db import models
from django.template.defaultfilters import slugify


LANGUAGES = (
    ('en', 'Inglês'),
    ('pt-br', 'Português'),
)


def get_file_path(instance, filename):
    return os.path.join(str(instance.slug), filename)


class Episode(models.Model):

    slug = models.SlugField(max_length=255)
    video = models.FileField(upload_to=get_file_path)
    subtitles = models.FileField(upload_to=get_file_path, blank=True, null=True, default=None)
    number = models.IntegerField()

    watched = models.IntegerField(default=0)

    def length(self, format='default'):
        video = cv2.VideoCapture(self.video.path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

        time = timedelta(seconds=frames//fps) if fps else timedelta(seconds=0)
        hour = time.seconds // 3600
        minutes = (time.seconds // 60) % 60
        seconds = time.seconds
        
        if format == 'default':
            return f"{hour}h {minutes}min" if hour else f"{minutes}min"
        elif format == 'minutes':
            return time.seconds // 60
        else:
            return (
                format.replace('%H', hour)
                      .replace('%M', minutes)
                      .replace('%S', seconds)
            )

    @property
    def length_minutes(self):
        return self.length(format='minutes')

    @property
    def watched_minutes(self):
        return self.watched // 60
            
    @property
    def title(self):
        return os.path.basename(self.video.name).split('.')[1].replace('_', ' ')

    @property
    def serie(self):
        return Serie.objects.get(slug=self.slug)

    @property
    def mimetype(self):
        return guess_type(self.video.path)[0]

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def percent_watched(self):
        return round((self.watched//60) / self.length_minutes * 100)

    def __str__(self):
        return f'T{self.serie.season}:E{self.number} "{self.title}"'


class Movie(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    poster = models.ImageField(upload_to=get_file_path)
    video = models.FileField(upload_to=get_file_path)
    lang = models.CharField(max_length=255, choices=LANGUAGES)
    subtitles = models.FileField(upload_to=get_file_path, blank=True, null=True, default=None)

    watched = models.IntegerField(default=0)

    def length(self, format='default'):
        video = cv2.VideoCapture(self.video.path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

        time = timedelta(seconds=frames//fps) if fps else timedelta(seconds=0)
        hour = time.seconds // 3600
        minutes = (time.seconds // 60) % 60
        seconds = time.seconds
        
        if format == 'default':
            return f"{hour}h {minutes}min" if hour else f"{minutes}min"
        elif format == 'minutes':
            return time.seconds // 60
        else:
            return (
                format.replace('%H', hour)
                      .replace('%M', minutes)
                      .replace('%S', seconds)
            )

    @property
    def length_minutes(self):
        return self.length(format='minutes')

    @property
    def watched_minutes(self):
        return self.watched // 60

    @property
    def mimetype(self):
        return guess_type(self.video.path)[0]

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def percent_watched(self):
        return round((self.watched//60) / self.length_minutes * 100)
    
    @property
    def absolute_url(self):
        return f'/watch/movie/{self.slug}/'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        
        for file in os.listdir(Path(self.video.path).parent.absolute()):
            os.remove(file)
            
        Path(self.video.path).parent.rmdir()

    def __str__(self):
        return self.title

class Serie(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    poster = models.ImageField(upload_to=get_file_path)
    lang = models.CharField(max_length=255, choices=LANGUAGES)
    season = models.IntegerField(default=1)
    episodes = models.ManyToManyField(Episode)

    watched_last = models.IntegerField(default=1)

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def last_episode(self):
        return self.episodes.get(number=self.watched_last)
    
    @property
    def absolute_url(self):
        return f'/watch/series/{self.slug}/{self.watched_last}/'

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title} {self.season} Temporada")
        super(Serie, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Serie, self).delete(*args, **kwargs)
        
        for episode in self.episodes.all():
            episode.delete()

        for file in os.listdir(Path(self.poster.path).parent.absolute()):
            os.remove(file)
            
        Path(self.poster.path).parent.rmdir()

    def __str__(self):
        return self.title
