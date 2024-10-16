import requests
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Selenium-based video scraping (use this for platforms requiring dynamic page interaction)
def selenium_download_video(video_url):
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode

    # Automatically download and set up the correct version of ChromeDriver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        driver.get(video_url)
        driver.implicitly_wait(10)  # Adjust the wait time if necessary

        # Example: Find the video element or direct video link
        video_element = driver.find_element('tag name', 'video')
        video_src = video_element.get_attribute('src')

        return video_src  # Return the direct video URL
    except Exception as e:
        print(f"Error fetching video: {e}")
    finally:
        driver.quit()

    return None


# Function to use yt-dlp for downloading videos
def yt_dlp_download_video(video_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            if 'formats' in info_dict:
                video_download_url = info_dict['formats'][0]['url']
                return video_download_url
    except Exception as e:
        print(f"Error fetching video: {e}")

    return None

# Main function that decides which method to use based on the platform
def download_video(video_url):
    if "tiktok.com" in video_url:
        return selenium_download_video(video_url)  # Use Selenium for TikTok
    elif "facebook.com" in video_url:
        return selenium_download_video(video_url)  # Use Selenium for Facebook
    else:
        return yt_dlp_download_video(video_url)  # Use yt-dlp for others

def video_download(request):
    download_link = None
    error_message = None

    if request.method == "POST":
        video_url = request.POST.get('url')

        try:
            download_link = download_video(video_url)

            if download_link is None:
                error_message = "Could not fetch the video. Please check the URL or the platform."
        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render(request, 'vd_app/video_download.html', {'download_link': download_link, 'error_message': error_message})

def scrape_video(request):
    return render(request, "vd_app/video_download.html")

def how_to(request):
    return render(request, 'vd_app/how_to.html')

def contact_us(request):
    return render(request, 'vd_app/contact_us.html')





"""
import youtube_dl
import instaloader
from instaloader.exceptions import BadResponseException, LoginRequiredException
from playwright.sync_api import sync_playwright
import yt_dlp
import time


# Scraping YouTube video using yt-dlp
def scrape_youtube_video(url):
    ydl_opts = {
        'format': 'best',  # Choose format, 'best' or others
        'quiet': True,     # Suppress terminal output
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)  # Get video info without downloading
        video_url = info_dict.get('url')
        video_title = info_dict.get('title')
        video_thumbnail = info_dict.get('thumbnail')
        video_description = info_dict.get('description')

    return {
        'video_url': video_url,
        'title': video_title,
        'thumbnail_url': video_thumbnail,
        'description': video_description,
        'platform': 'YouTube',
    }


# Function to scrape Instagram using Instaloader
def scrape_instagram_video_instaloader(url):
    L = instaloader.Instaloader()
    try:
        # Extract shortcode from Instagram URL
        shortcode = url.split('/')[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        video_url = post.video_url
        video_title = post.title or 'Instagram Video'
        return {
            'video_url': video_url,
            'title': video_title,
            'platform': 'Instagram'
        }
    except (BadResponseException, LoginRequiredException) as e:
        print(f"Error fetching Instagram video with Instaloader: {str(e)}")
        return None

# Fallback function to scrape Instagram using yt-dlp
def scrape_instagram_video_yt_dlp(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'your_cookie_here',  # Optional: Pass cookies if needed
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)
            return {
                'video_url': video_info.get('url'),
                'title': video_info.get('title', 'Instagram Video'),
                'platform': 'Instagram'
            }
    except Exception as e:
        print(f"Error fetching Instagram video with yt-dlp: {str(e)}")
        return None


# Main function to scrape Instagram video, trying Instaloader first, yt-dlp as fallback
def scrape_instagram_video(url):
    video_info = scrape_instagram_video_instaloader(url)
    if not video_info:
        # If Instaloader fails, try yt-dlp
        video_info = scrape_instagram_video_yt_dlp(url)
    return video_info



# Scraping TikTok video using yt-dlp
def scrape_tiktok_video(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'TikTok Video'),
                'video_url': info.get('url'),
                'thumbnail_url': info.get('thumbnail', ''),
                'platform': 'TikTok',
            }
    except Exception as e:
        print(f"Error fetching TikTok video: {str(e)}")
        return None
"""
"""
# Scraping Facebook video using yt-dlp
def scrape_facebook_video(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title'),
                'video_url': info.get('url'),
                'thumbnail_url': info.get('thumbnail'),
                'platform': 'Facebook',
            }
        except Exception as e:
            print(f"Error fetching Facebook video: {str(e)}")
            return None


# Scraping Twitter video using yt-dlp
def scrape_twitter_video(url):
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'best',  # Choose best quality by default
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)
            return {
                'title': video_info.get('title', 'Twitter Video'),
                'video_url': video_info['url'],
                'platform': 'Twitter',
                'formats': video_info.get('formats', [])  # Include formats for quality selection
            }
    except Exception as e:
        print(f"Error scraping Twitter video: {str(e)}")
        return None
"""
