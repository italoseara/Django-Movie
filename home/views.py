import os
import re
import json
from mimetypes import guess_type
from wsgiref.util import FileWrapper

from django.http.response import HttpResponse, StreamingHttpResponse
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Movie, Serie, Episode
from .forms import MovieForm, SerieForm


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


# Views
@method_decorator(csrf_exempt, name='dispatch')
class HomeView(ListView):
    model = Movie

    def get_context_data(self, **kwargs):
        keep_watching = []

        for serie in Serie.objects.all():
            episode = serie.episodes.get(number=serie.watched_last)
            if (
                (episode.watched != 1 and 2 < episode.percent_watched) 
                or (episode.watched and episode.percent_watched < 95)
            ):
                
                keep_watching.append(serie)

        for movie in Movie.objects.all():
            if movie.watched and 2 < movie.percent_watched < 95:
                keep_watching.append(movie)

        keep_watching.sort(key=lambda x: x.title)
        
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'serie_list': Serie.objects.all(),
            'keep_watching': keep_watching
        })
        return context


@method_decorator(csrf_exempt, name='dispatch')
class WatchMovieView(DetailView):
    model = Movie


@method_decorator(csrf_exempt, name='dispatch')
class WatchSeriesView(DetailView):
    model = Serie

    def get_context_data(self, **kwargs):
        serie = Serie.objects.get(slug=self.kwargs['slug'])
        
        context = super().get_context_data(**kwargs)
        context.update({
            'episode': serie.episodes.get(number=self.kwargs['episode']),
        })

        serie.watched_last = self.kwargs['episode']
        serie.save()
        return context


# Forms
def add_movie(request):

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/browse/')
        else:
            print(form._errors)
    else:
        form = MovieForm
        
    return render(request, 'home/form.html', {'form': form, 'is_serie': False, 'title': 'Adicionar Filme'})


def add_serie(request):
    
    if request.method == 'POST':
        form = SerieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            for index, file in enumerate(request.FILES.getlist('episodes')):
                episode = Episode(
                    slug=slugify(f'{form.cleaned_data["title"]} {form.cleaned_data["season"]} Temporada'), 
                    video=file,
                    subtitles=request.FILES.getlist('subtitles')[index],
                    number=index+1
                )
                episode.save()

                form.instance.episodes.add(episode)

            form.save()
                
            return HttpResponseRedirect('/browse/')
        else:
            print(form._errors)
    else:
        form = SerieForm
        
    return render(request, 'home/form.html', {'form': form, 'is_serie': True, 'title': 'Adicionar Série'})


# API
def update_video_time(request):
    
    if request.method == 'POST':
        video_id = request.POST.get('videoId')
        video_type = request.POST.get('videoType')
        watched_time = round(float(request.POST.get('time')))
        video = eval(video_type).objects.get(id=video_id)
        video.watched = watched_time
        video.save()
        
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')


def clear_watching(request):

    if request.method == 'POST':
        for serie in Serie.objects.all():
            for episode in serie.episodes.all():
                episode.watched = 0
                episode.save()
                
            serie.watched_last = 1
            serie.save()

        for movie in Movie.objects.all():
            movie.watched = 0
            movie.save()

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            
            if data:
                return data
            
            raise StopIteration()
        
        else:
            if self.remaining <= 0:
                raise StopIteration()
            
            data = self.filelike.read(min(self.remaining, self.blksize))
            
            if not data:
                raise StopIteration()
            
            self.remaining -= len(data)
            return data


def stream_video(request, path):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = guess_type(path)
    content_type = content_type or 'application/octet-stream'
    
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        
        if last_byte >= size:
            last_byte = size - 1

        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
        
    resp['Accept-Ranges'] = 'bytes'
    return resp