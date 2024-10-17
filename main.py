class Main:

    env_path = "/home/user/Documents/spos.env"
    load_dotenv(dotenv_path=env_path)

    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
    OUTPUT_FILE_NAME = "track_info.csv"

    PLAYLIST_LINK = playlist

    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)  

    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
        playlist_uri = match.groups()[0]
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...") 

    #getting playlist name 
    playlist_details = session.playlist(playlist_uri)
    playlist_name = playlist_details["name"]

    #making a new directory to store songs 
    username = os.getlogin()
    parent_path = "/home/" + username + "/Music/"
    path = os.path.join(parent_path,playlist_name)
    if os.path.exists(path):
         print("Directory already exists! Making it the download path...")
    else:
         os.mkdir(path)

    # Initialize variables for pagination
    offset = 0
    limit = 100  # The maximum limit per request
    all_tracks = []

    while True:
        # Retrieve tracks in batches with pagination
        tracks = session.playlist_tracks(playlist_uri, offset=offset, limit=limit)["items"]

        if not tracks:
            break

        all_tracks.extend(tracks)
        offset += limit

    with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        # write header column names
        writer.writerow(["track", "artist"])

        # extract name and artist
        for track in all_tracks:
            name = track["track"]["name"]
            artists = ", ".join(
            [artist["name"] for artist in track["track"]["artists"]]
        )

            # write to csv
            writer.writerow([name, artists])

