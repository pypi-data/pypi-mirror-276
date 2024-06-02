# tanjiro/youtube.py

import os
from yt_dlp import YoutubeDL

def download_video(url, save_path):
    """
    Downloads a video from YouTube and saves it to the specified path.

    Parameters:
    url (str): The URL of the YouTube video to download.
    save_path (str): The directory where the video will be saved.

    Returns:
    str: The path to the downloaded video.
    """
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Choose the best quality available
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save with the video title as the filename
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)

    # Return the path to the downloaded video file
    return os.path.join(save_path, ydl.prepare_filename(info_dict))
