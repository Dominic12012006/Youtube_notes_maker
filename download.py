import yt_dlp
import os

ffmpeg_bin=r'C:\ffmpeg\ffmpeg-2025-05-26-git-43a69886b2-full_build\bin'
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio',
        'ffmpeg_location':ffmpeg_bin,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        # Manually build final filename
        filename = ydl.prepare_filename(result)
        # Replace original extension with .wav
        path = os.path.splitext(filename)[0] + '.wav'
        return path
