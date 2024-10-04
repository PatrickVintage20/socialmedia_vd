import yt_dlp
import os

def download_video(video_url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',  # Save file as title of the video
            'noplaylist': True,  # Don't download playlists
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'video')  # Fallback to 'video'
            video_ext = info_dict.get('ext', 'mp4')  # Fallback to 'mp4'
            file_path = f"{video_title}.{video_ext}"  # Construct the file path

        print(f"Downloaded video to: {file_path}")  # Debugging line
        return file_path
    except Exception as e:
        print(f"Error downloading video: {e}")  # More detailed error
        return None
