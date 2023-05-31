from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from django.urls import include, path
from catdogsite import settings
from .views import *

urlpatterns = [
    path('reisenbestadmin/', admin.site.urls),
    path("", main, name='home'),
    path("stats/", stats, name='stats'),
    path('show_stats/', show_stats, name='show_stats'),
    path("about/", about, name='about'),
    path("feedback/", feedback, name='feedback'),
    path("recognizeimg/", recognize, name='recognize'),
    path('after_rec/<int:tmp_for_database_object>/', after_recognize, name='after_recognize'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = pageNotFound

