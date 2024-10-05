import requests
from django.http import JsonResponse
from django.shortcuts import render

def download_video_view(request):
    if request.method == "POST":
        video_url = request.POST.get('url')
        filename = request.POST.get('filename', 'video_download')  # Default filename
        
        api_url = "https://social-media-video-downloader.p.rapidapi.com/smvd/get/all"
        headers = {
            "x-rapidapi-host": "social-media-video-downloader.p.rapidapi.com",
            "x-rapidapi-key": "edb9006024mshc614a8e04873cecp1b25f4jsna580f65d63b4"  # Replace with your actual API key
        }
        params = {
            "url": video_url,
            "filename": filename
        }

        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            video_data = response.json()
            return JsonResponse(video_data)
        else:
            return JsonResponse({"error": "Failed to download video"}, status=response.status_code)

    return render(request, 'download_video.html')  # Render your form or page for input
"""
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from urllib.parse import urlencode, unquote_plus
from .forms import VideoURLForm
from .playwright_scrapers import (
    scrape_facebook_video, scrape_youtube_video, 
    scrape_twitter_video
)
import yt_dlp

from django.shortcuts import render
from .utils import get_video_info 



# View to handle video URL form and display video information
def video_download_view(request):
    if request.method == 'POST':s
        form = VideoURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            # Determine the platform and call the appropriate scraping function
            video_info = None
            if "youtube.com" in url or "youtu.be" in url:
                video_info = scrape_youtube_video(url)
            elif "instagram.com" in url:
                video_info = scrape_instagram_video(url)  # Combined method for Instagram
            elif "tiktok.com" in url:
                video_info = scrape_tiktok_video(url)
            elif "facebook.com" in url:
                video_info = scrape_facebook_video(url)
            elif "twitter.com" in url:
                video_info = scrape_twitter_video(url)

            # Handle cases where video_info is None
            if video_info is None:
                return render(request, 'vd_app/video_download.html', {'form': form, 'error': "Video not found or unsupported platform."})

            # Prepare for rendering the video information
            video_info['encoded_video_url'] = urlencode({'url': video_info['video_url']})
            return render(request, 'vd_app/video_info.html', {'video_info': video_info})

    else:
        form = VideoURLForm()
    return render(request, 'vd_app/video_download.html', {'form': form})


# View to handle the actual video download process
def download_video_view(request, url):
    try:
        # Unquote the URL in case it's URL encoded
        video_url = unquote_plus(url)
        print(f"Attempting to download video from URL: {video_url}")

        # Set up options for yt-dlp
        ydl_opts = {
            'format': 'best',  # Select best video quality
            'quiet': True,  # Suppress unnecessary yt-dlp output
            'noplaylist': True,  # Only download single video if it's part of a playlist
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Use yt-dlp to get video information without downloading
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', 'video')
            video_extension = info_dict.get('ext', 'mp4')
            direct_video_url = info_dict.get('url')  # Get the direct video URL

            # Use StreamingHttpResponse to stream the video to the user
            response = StreamingHttpResponse(ydl.urlopen(direct_video_url), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="{video_title}.{video_extension}"'
            return response

    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return HttpResponse(f"Error downloading video: {str(e)}", status=400)

 # Import your function to fetch video info


def video_download(request):
    error = None
    if request.method == 'POST':
        video_url = request.POST.get('url')
        try:
            # Fetch video information
            video_info = get_video_info(video_url)
            # Pass video info to the video_info template
            return render(request, 'vd_app/video_info.html', {'video_info': video_info})
        except Exception as e:
            error = str(e)

    return render(request, 'vd_app/video_download.html', {'error': error})



def Home(request):
    return render(request, "vd_app/video_download.html")

def how_to(request):
    return render(request, 'vd_app/how_to.html')

def contact_us(request):
    return render(request, 'vd_app/contact_us.html')
    
"""


