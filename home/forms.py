from django import forms
from django.forms import ModelForm

from .models import Movie, Serie


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'poster', 'lang', 'video', 'subtitles')

        labels = {
            'title': 'Título',
            'slug': '',
            'poster': 'Poster',
            'lang': 'Idioma',
            'video': 'Vídeo',
            'subtitles': 'Legendas',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'lang': forms.Select(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
            'subtitles': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SerieForm(ModelForm):
    class Meta:
        model = Serie
        fields = ('title', 'poster', 'lang', 'season')

        labels = {
            'title': 'Título',
            'slug': '',
            'poster': 'Poster',
            'lang': 'Idioma',
            'season': 'Temporada',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'lang': forms.Select(attrs={'class': 'form-control'}),
            'season': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        