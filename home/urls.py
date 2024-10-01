from django.contrib import admin
from django.urls import path, include
from . views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('', home_view, name='home'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
