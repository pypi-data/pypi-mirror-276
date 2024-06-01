# tanjiro/youtube.py

from pytube import YouTube

def download_video(url, save_path):
    """
    Download a YouTube video.

    Parameters:
    url (str): The URL of the YouTube video to download.
    save_path (str): The directory path to save the downloaded video.

    Returns:
    str: Path to the downloaded video file.

    Usage:
    ------
    from tanjiro import youtube

    # Provide the URL of the YouTube video and the directory to save the video
    video_path = youtube.download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "videos/")

    print(f"Video downloaded to: {video_path}")
    """
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video_path = video.download(save_path)
    return video_path
