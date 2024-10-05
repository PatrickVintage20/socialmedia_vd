# vd_app/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.video_download, name='video_download'),
    path('download/<str:filename>/', views.download_video, name='download_video'),
]
