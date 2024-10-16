# vd_app/urls.py

from django.urls import path
from . import views
from .views import video_download,download_video, scrape_video, how_to, contact_us


urlpatterns = [ 
    path('', views.video_download, name='video_download'),  # Main video downloader
    path('download/<str:filename>/', views.download_video, name='download_video'),  # Correct path for downloading the video
    path('how-to/', views.how_to, name='how_to'),  # How to use page
    path('contact-us/', views.contact_us, name='contact_us'),  # Contact us page

    #path('download/<str:filename>/', views.download_video, name='download_video'),
    #path('download/', views.video_download, name='video_download'),
    #path('stream/', views.stream_video, name='stream_video'), # View for scraping info (if needed)

]
