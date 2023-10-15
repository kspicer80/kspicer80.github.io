---
title: "What Kind of Songs Do I Like? Goofing Around with the Spotify API and My Bizarre Music Tastes"
date: 2023-10-15 00:01:00
draft: true
toc: false
tags:
  - API
  - apis
  - python
  - requests
  - spotify
  - data analysis
  - requests library
  - pandas
  - seaborn
  - data visualization
  - data analysis
  - spotipy library
---

I was having a conversation with my most favorite student that I've ever had in my entire career as a teacher aa while back and we got to chatting about my little pattern of sending her songs I like from the "Discover Weekly" and "Release Radar" playlists that come my way via Spotify. She and I seem to have very few similarities when it comes to music. She likes to say that I have somewhat "girlish" music tastes (not meant as a pejorative, far from it, at least, I think!), but I like to think that I like certain songs based on how easy it is for me to move my body in tune with them. I figure I would do a little testing to see if my intuitions were correct or not. So, in order to do just that, off we go.

The first step was hop over to the [Spotify site for developers](https://developer.spotify.com). You can follow some of the really nice tutorials on accessing the API (see [here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)) ... thus, with an application sent up, we should be good to go with accessing the API via Python. On that note, we will want to install the "spotipy" library (available (here)[https://spotipy.readthedocs.io/en/2.22.1/]). With that installed, we can start some code ourselves. We need a way to traverse the entirety of my "Liked Songs" playlist. As per usual, let's write some code:

```python
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os

def user_playlist_tracks_full(spotify_connection, user, playlist_id=None, fields=None, market=None):
    """ Get full details of the tracks of a playlist owned by a user.
        https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/

        Parameters:
            - user - the id of the user
            - playlist_id - the id of the playlist
            - fields - which fields to return
            - market - an ISO 3166-1 alpha-2 country code.
    """

    # first run through also retrieves total no of songs in library
    response = spotify_connection.user_playlist_tracks(user, playlist_id, fields=fields, limit=100, market=market)
    results = response["items"]

    # subsequently runs until it hits the user-defined limit or has read all songs in the library
    while len(results) < response["total"]:
        response = spotify_connection.user_playlist_tracks(
            user, playlist_id, fields=fields, limit=100, offset=len(results), market=market
        )
        results.extend(response["items"])
```

Now that we have that function defined, we can dig a little deeper into how we want/are going to use the spotipy library. Spotify has all kinds definitions, ideas, data, explanations for their key numbers that describe their song]  Spotify's numbers [here](https://developer.spotify.com/documentation/web-api/reference/get-audio-features). I am interested in figuring out how well my own musical sensitivity either converges or strongly diverges with those of other Spotify listeners, instead. Here is some code to grab every singe song from your "Liked Songs" playlist

``` python
os.environ['SPOTIPY_CLIENT_ID'] = '' # unique client_id here
os.environ['SPOTIPY_CLIENT_SECRET'] = '' # unique client_secret here
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

scope = "user-library-read user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
print(sp.me())

with open('saved_tracks.json', 'r') as infile:
    saved_tracks = json.load(infile)
```

``` python 
tracks_with_features = []
batch_size = 50
for i in range(0, len(saved_tracks), batch_size):
    batch = saved_tracks[i:i+batch_size]
    track_uris = [item["track"]["uri"] for item in batch]
    track_infos = sp.tracks(track_uris)["tracks"]
    audio_features = sp.audio_features(track_uris)
    for j in range(len(batch)):
        track = batch[j]["track"]
        track_uri = track["uri"]
        track_info = track_infos[j]
        audio_feature = audio_features[j]
        track_with_features = {
            "name": track_info["name"],
            "artist": track_info["artists"][0]["name"],
            "album": track_info["album"]["name"],
            "uri": track_uri,
            "added_at": batch[j]["added_at"],
            "danceability": audio_feature["danceability"],
            "energy": audio_feature["energy"],
            "key": audio_feature["key"],
            "loudness": audio_feature["loudness"],
            "mode": audio_feature["mode"],
            "speechiness": audio_feature["speechiness"],
            "acousticness": audio_feature["acousticness"],
            "instrumentalness": audio_feature["instrumentalness"],
            "liveness": audio_feature["liveness"],
            "valence": audio_feature["valence"],
            "tempo": audio_feature["tempo"],
            "duration_ms": audio_feature["duration_ms"],
            "time_signature": audio_feature["time_signature"]
        }
        tracks_with_features.append(track_with_features)

with open('saved_tracks_with_features.json', 'w') as outfile:
    json.dump(tracks_with_features, outfile, indent=4)

print(f"Saved {len(tracks_with_features)} tracks with features to saved_tracks_with_features.json")
```