# vd_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_download_view, name='video_download'),
    path('download/<path:url>/', views.download_video_view, name='download_video'),  # Notice <path:url> here for full URLs
]
