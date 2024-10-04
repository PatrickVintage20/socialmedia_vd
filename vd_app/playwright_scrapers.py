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


"""
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
