# vd_app/utils.py

def get_video_info(video_url):
    # Your logic to fetch video information goes here
    # Return a dictionary or an object with the necessary video info
    return {
        'title': 'Sample Video',
        'thumbnail_url': 'https://example.com/thumbnail.jpg',
        'description': 'This is a sample description of the video.',
        'platform': 'YouTube',
        'formats': [
            {'format_id': '1', 'format_note': '720p', 'resolution': '1280x720'},
            {'format_id': '2', 'format_note': '480p', 'resolution': '854x480'},
            # Add more formats as needed
        ],
        'video_url': video_url
    }
