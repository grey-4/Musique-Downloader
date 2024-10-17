import sys
import getopt
import pytube
from youtubesearchpython import VideosSearch 
from moviepy.editor import AudioFileClip
import os


# Define your search query
    search_query = song
# # Create a VideosSearch object
    videos_search = VideosSearch(search_query, limit=1)

# # Get the search results
    results = videos_search.result()

    for video in results["result"]:
        video_title = video["title"]
        video_id = video["id"]
        video_url = "https://www.youtube.com/watch?v=" + video_id
        print(f"Title: {video_title}")
        print(f"Video URL: {video_url}")

    try:
     # Get the YouTube video
        yt = pytube.YouTube(video_url)

     # Get the highest quality audio stream
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        if audio_stream:
         # Download the audio
             audio_path = audio_stream.download(output_path="/home/grey/Music/Liked Songs/")

         # Convert the audio from MP4 to MP3
             audio_path_mp3 = audio_path.replace(".mp4", ".mp3")
             audio_clip = AudioFileClip(audio_path)
             audio_clip.write_audiofile(audio_path_mp3)
             audio_clip.close()

         # Clean up the downloaded files
             os.remove(audio_path)

             print("Audio downloaded in MP3 format with the highest quality.")
        else:
             print("No MP3 audio streams available for download.")

    except pytube.exceptions.RegexMatchError as e:
         print("Regex match error:", e)
    except Exception as e:
         print("An error occurred:", e)
