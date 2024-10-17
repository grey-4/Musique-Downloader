import main
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import pytube
from youtubesearchpython import VideosSearch
from moviepy.editor import AudioFileClip
import os

count = 1

#import the csv file with songs and artists name 
with open('/home/grey/projects/spos/track_info.csv',newline='') as f:
     reader = csv.reader(f)
     data = list(reader)


def get_download(video_url):
    # Get the YouTube video
     yt = pytube.YouTube(video_url)

     # Get the highest quality audio stream
     audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

     if audio_stream:
          # Download the audio
          audio_path = audio_stream.download(output_path = main.path + "/")

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
    
def resume_search(data, count):
    try:
        with open('resume.txt', 'r') as pos:
            position_str = pos.read().strip()
            if position_str:
                position = int(position_str)
                os.remove('resume.txt')
                return position,data[position][0] + ' by ' + data[position][1]
    except FileNotFoundError:
        return count,data[count][0] + ' by ' + data[count][1]


def get_url(search):
    results = search.result()
    for video in results["result"]:
        video_title = video["title"]
        video_id = video["id"]
        video_url = "https://www.youtube.com/watch?v=" + video_id
        print(f"Title: {video_title}")
        return video_url


while count < len(data):
    count, search_query = resume_search(data, count)

    # Create a VideosSearch object
    videos_search = VideosSearch(search_query, limit=1)

    # Get the search results
    url = get_url(videos_search)

    try:
        print(count)
        get_download(url)
        count += 1

    except KeyboardInterrupt:
        with open('resume.txt', 'w') as last:
            last.write(str(count))
        break
    
    except Exception:
        print("Exception")
        search = VideosSearch(search_query,limit=5)
        get_url(search)
