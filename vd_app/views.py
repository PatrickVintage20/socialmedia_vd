import yt_dlp
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import os
import tempfile
import shutil
import concurrent.futures
import uuid  # For generating unique filenames
from django.conf import settings  # Import settings for cookies path

# Directory for temporary video storage
DOWNLOAD_DIR = tempfile.gettempdir()

# Check if ffmpeg is installed and available
def is_ffmpeg_installed():
    try:
        yt_dlp.utils.check_executable('ffmpeg', ['-version'])
        return True
    except yt_dlp.utils.DownloadError:
        return False

# yt-dlp download function with cookies and unique filename handling
def yt_dlp_download_video(video_url, output_filename):
    unique_filename = f"{uuid.uuid4()}.mp4"  # Generate unique filename for each request
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, unique_filename),  # Save with unique filename
        'format': 'best',
        'quiet': True,
        'noplaylist': True,
        'cookies': settings.COOKIES_FILE_PATH,  # Pass cookies file for all requests from settings
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}] if is_ffmpeg_installed() else [],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_filename = ydl.prepare_filename(info_dict)  # Path to the downloaded video
            return {
                'title': info_dict.get('title', 'Unknown Title'),
                'thumbnail': info_dict.get('thumbnail', ''),
                'description': info_dict.get('description', 'No description available.'),
                'filename': video_filename  # Use the correct filename here
            }
    except yt_dlp.utils.DownloadError as e:
        raise Exception(f"Download failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching video: {str(e)}")

# Main view function for video downloading
def video_download(request):
    video_info = {}

    if request.method == "POST":
        video_url = request.POST.get('url')
        platform = get_platform_from_url(video_url)

        try:
            output_filename = platform + "_video.mp4"
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(yt_dlp_download_video, video_url, output_filename)
                video_info = future.result()

        except Exception as e:
            video_info['error'] = str(e)

    return render(request, 'vd_app/video_download.html', {'video_info': video_info})

# File download function
def download_video(request, filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return JsonResponse({'error': 'File not found.'})

# Determine platform from URL
def get_platform_from_url(url):
    """Determines the platform from the URL."""
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "facebook.com" in url:
        return "facebook"
    elif "twitter.com" in url:
        return "twitter"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "instagram.com" in url:
        return "instagram"
    return "unknown"

# Other view functions
def scrape_video(request):
    return render(request, "vd_app/video_download.html")

def how_to(request):
    return render(request, 'vd_app/how_to.html')

def contact_us(request):
    return render(request, 'vd_app/contact_us.html')




"""

import yt_dlp
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
import requests
import os


# Extract video stream URL using yt-dlp
def get_video_stream(video_url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Combine best video and best audio
        'quiet': True,
        'noplaylist': True,
        'outtmpl': '/dev/null',  # Don't save the file
        'progress_hooks': [lambda d: print(d)],  # Hook to see progress (optional)
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        # Get the URL for the video + audio combined format
        for f in info_dict['formats']:
            if f['ext'] == 'mp4' and f['acodec'] != 'none' and f['vcodec'] != 'none':
                video_url = f['url']  # Select format that contains both audio and video
                return video_url
        raise Exception("No suitable video format found.")



# Handle video download page
def video_download(request):
    video_info = {}

    if request.method == "POST":
        video_url = request.POST.get('url')
        platform = get_platform_from_url(video_url)

        try:
            stream_url = get_video_stream(video_url)  # Get the stream URL
            video_info = {
                'url': stream_url,
                'title': 'Video Title',  # Optionally add the title from info_dict
            }
        except Exception as e:
            video_info['error'] = str(e)

    return render(request, 'vd_app/video_download.html', {'video_info': video_info})



def stream_video(request):
    video_url = request.GET.get('url')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': video_url  # Include referer header
    }

    try:
        # Make a request to the video URL with proper headers
        response = requests.get(video_url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)

        # Stream the video content directly to the user
        return StreamingHttpResponse(response.iter_content(chunk_size=8192), content_type="video/mp4")

    except requests.exceptions.RequestException as e:
        # Log the error and show an error page
        print(f"Error fetching the video: {e}")
        return render(request, 'vd_app/error.html', {'error_message': 'Unable to stream the video. Please try again.'})


# Platform detection
def get_platform_from_url(url):
    Determines the platform from the URL
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "facebook.com" in url:
        return "facebook"
    elif "twitter.com" in url:
        return "twitter"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "instagram.com" in url:
        return "instagram"
    return "unknown"


# Other views
def scrape_video(request):
    return render(request, "vd_app/video_download.html")

def how_to(request):
    return render(request, 'vd_app/how_to.html')

def contact_us(request):
    return render(request, 'vd_app/contact_us.html')






import requests
from django.shortcuts import render
from django.http import JsonResponse

# Your RapidAPI key and host
RAPIDAPI_KEY = "edb9006024mshc614a8e04873cecp1b25f4jsna580f65d63b4"
RAPIDAPI_HOST = "social-media-video-downloader.p.rapidapi.com"

def video_download_view(request):
    if request.method == 'POST':
        video_url = request.POST.get('url')

        # Check if URL is provided
        if not video_url:
            return render(request, 'vd_app/video_download.html', {'error': 'Please provide a valid video URL.'})

        # Prepare headers for the RapidAPI request
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }

        # Prepare the request URL
        api_url = f"https://{RAPIDAPI_HOST}/smvd/get/all?url={video_url}"

        try:
            # Make a GET request to the RapidAPI endpoint
            response = requests.get(api_url, headers=headers)
            data = response.json()

            # Check if response contains the video data
            if 'data' in data and data['data'].get('download_url'):
                video_data = {
                    'download_url': data['data']['download_url'],
                    'platform': data['data']['platform'],
                    'title': data['data']['title'],
                }
                return render(request, 'vd_app/video_download.html', {'video': video_data})

            else:
                # Error handling for invalid response
                return render(request, 'vd_app/video_download.html', {'error': 'Unable to retrieve video information. Please try again.'})

        except Exception as e:
            # Handle any exceptions such as network issues
            return render(request, 'vd_app/video_download.html', {'error': f"An error occurred: {str(e)}"})

    return render(request, 'vd_app/video_download.html')



RAPIDAPI_HOST = 'social-media-video-downloader.p.rapidapi.com'
RAPIDAPI_KEY = 'edb9006024mshc614a8e04873cecp1b25f4jsna580f65d63b4'  # Replace with your actual RapidAPI key

def download_video_view(request, url):
    if request.method == 'GET':
        try:
            # Make request to RapidAPI to download the video
            response = requests.get(
                f'https://{RAPIDAPI_HOST}/smvd/get/all',
                headers={
                    'x-rapidapi-host': RAPIDAPI_HOST,
                    'x-rapidapi-key': RAPIDAPI_KEY,
                },
                params={'url': url}
            )

            # Check if the response from API is successful
            if response.status_code == 200:
                video_data = response.json()  # Assuming the response is in JSON format
                # Pass video data to the template
                return render(request, 'vd_app/video_download.html', {'video_data': video_data})

            else:
                return render(request, 'vd_app/video_download.html', {'error': 'Failed to download video. Try again later.'})
        except Exception as e:
            return render(request, 'vd_app/video_download.html', {'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method. Use GET instead.'}, status=400)


def Home(request):
    return render(request, "vd_app/video_download.html")

def how_to(request):
    return render(request, 'vd_app/how_to.html')

def contact_us(request):
    return render(request, 'vd_app/contact_us.html')





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


"""


