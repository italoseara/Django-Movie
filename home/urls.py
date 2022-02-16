from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

from . import views

app_name = 'home'

urlpatterns = [
    path('', lambda request: HttpResponseRedirect('browse/'), name='home'),
    path('browse/', views.HomeView.as_view(), name='movie_list'),
    
    path('watch/movie/<slug:slug>/', views.WatchMovieView.as_view(), name='movie_detail'),
    path('watch/series/<slug:slug>/<int:episode>/', views.WatchSeriesView.as_view(), name='serie_detail'),
    
    path('add/movie/', views.add_movie, name='add_movie'),
    path('add/serie/', views.add_serie, name='add_serie'),
    
    path('api/stream/<path:path>/', views.stream_video, name='stream_video'),
    path('api/update-video-time/', views.update_video_time, name='update_video_time'),
    path('api/clear-watching/', views.clear_watching, name='clear_watching'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
