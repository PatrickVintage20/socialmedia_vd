# vd_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('scrape_youtube/', views.scrape_youtube_video_view, name='scrape_youtube'),
    path('scrape_facebook/', views.scrape_facebook_video_view, name='scrape_facebook'),
    path('scrape_twitter/', views.scrape_twitter_video_view, name='scrape_twitter'),
    path('scrape_tiktok/', views.scrape_tiktok_video_view, name='scrape_tiktok'),
    path('scrape_instagram/', views.scrape_instagram_video_view, name='scrape_instagram'),
]