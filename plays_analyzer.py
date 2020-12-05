import json
import unittest
import os
import requests
import sqlite3
import spotipy
import spotipy.util as util
#from spotipy.oauth2 import SpotifyClientCredentials

# Names
# Timothy Wang - timwa@umich.edu
# Emily Choe - emchoe@umich.edu












#Spotipy API Info
CLIENT_ID = '9445bfc4e61f43ed83ec2782d464e42c'
CLIENT_SECRET = 'f7fb2a1c147744d1ade617f598eabc46'

#Today's Top Hits Playlist URI
#URI = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'

def write_json(spotify_json, spotify_dict):
    filepath = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(filepath, spotify_json)

    dumped = json.dumps(spotify_dict, indent=4, sort_keys=True)
    fw = open(file, 'w')
    fw.write(dumped)
    fw.close()

def find_song_ids(song_names):
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    BASE_URL = 'https://api.spotify.com/v1/search?q='

    tracks_ids = []

    for song in song_names:
        r = requests.get(BASE_URL + song + '&type=track&market=US&limit=1', headers=headers)
        r = r.json()
        write_json('spotify_tracks.json', r)

def get_todays_top_hits():
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    print(access_token)
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    BASE_URL = 'https://api.spotify.com/v1/'
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'
    r = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers)
    r = r.json()
    return r




def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    #write_json('spotify_top_hits.json', get_todays_top_hits())
    song_names = ['Wonder', 'positions', 'wish you were gay']
    find_song_ids(song_names)


if __name__ == "__main__":
    main()