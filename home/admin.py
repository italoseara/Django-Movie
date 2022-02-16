from django.contrib import admin

from .models import Episode, Movie, Serie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'length', 'lang')
    search_fields = ('title', 'slug', 'length', 'lang')

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'lang', 'season')
    search_fields = ('title', 'slug', 'lang', 'season')

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'number')
    search_fields = ('title', 'number')