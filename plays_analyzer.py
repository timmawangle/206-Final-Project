import json
import unittest
import os
import requests
import sqlite3
import spotipy
import spotipy.util as util

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
#from spotipy.oauth2 import SpotifyClientCredentials

# Names
# Timothy Wang - timwa@umich.edu
# Emily Choe - emchoe@umich.edu

#Spotipy API Info
CLIENT_ID = '9445bfc4e61f43ed83ec2782d464e42c'
CLIENT_SECRET = 'f7fb2a1c147744d1ade617f598eabc46'

#Today's Top Hits Playlist URI
#URI = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn


def write_json(spotify_json, spotify_dict):
    filepath = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(filepath, spotify_json)

    dumped = json.dumps(spotify_dict, indent=4, sort_keys=True)
    fw = open(file, 'w')
    fw.write(dumped)
    fw.close()


#YouTube API Info
API_KEY = 'AIzaSyD2NJk0i7N6SLl1SHzr1sOeMUuaDkcxRJ0'
Y_CLIENT_ID = '517531547391-96erielcd69ssc725h23vv6mhnv86d84.apps.googleusercontent.com'
Y_CLIENT_SECRET = 'sq9j0OQYjbgMH9mIkst-7q8O'
#Youtube
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def y_main():

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId="PLDIoUOhQQPlXr63I_vwF9GD8sAKh77dWU"
    )
    response = request.execute()

    print(response)


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

    tracks_list = []
    count = 0

    for song in song_names:
        r = requests.get(BASE_URL + song + '&type=track&market=US&limit=1', headers=headers)
        results = json.loads(r.text)
        tracks_list.append(results)
        write_json('spotify_tracks.json', tracks_list)
        #r = r.json()
        #write_json('spotify_tracks.json', r)
        #tracks_dict[song] = r
        if count < 25:
            count += 1
        else:
            break
    return tracks_list


def add_artists(cur, conn, index, name):
    cur.execute("INSERT INTO Artists(artist_id, name) VALUES (?,?)", (index, name))
    conn.commit()


def fill_spotify_tables(filename, cur, conn):
    filepath = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(filepath, filename)
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)

    unique_artists = []
    tracks_list = []

    count = 0
    for track in json_data:
        count += 1
        name = track['tracks']['items'][0]['name']
        artist = track['tracks']['items'][0]['artists'][0]['name']
        popularity_num = track['tracks']['items'][0]['popularity']
        #print(popularity_num)
        if artist not in unique_artists:
            unique_artists.append(artist)

        temp = (name, artist, popularity_num)
        #print(temp)
        tracks_list.append(temp)

    artist_ids = {}
    count = 0
    for artist in unique_artists:
        add_artists(cur, conn, count, artist)
        artist_ids[artist] = count
        count += 1

    count = 0
    for track in tracks_list:
        add_tracks(cur, conn, count, track[0], artist_ids[track[1]], track[2])
        count += 1


def create_artists_table(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Artists")
    cur.execute("CREATE TABLE Artists (artist_id INTEGER, name TEXT)")
    conn.commit()


def create_tracks_table(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Tracks")
    cur.execute("CREATE TABLE Tracks (track_id INTEGER, track_name TEXT, artist_id INTEGER, pop_index INTEGER)")
    conn.commit()


def add_tracks(cur, conn, track_index, track_name, artist_index, popularity_index):
    cur.execute("INSERT INTO Tracks(track_id, track_name, artist_id, pop_index) VALUES (?,?,?,?)", (track_index, track_name, artist_index, popularity_index))
    conn.commit()



def main():
    #write_json('spotify_top_hits.json', get_todays_top_hits())
    cur, conn = setUpDatabase('top_songs.db')
    song_names = ['Wonder', 'positions', 'wish you were gay', 'Billie Eilish - Therefore I am']
    find_song_ids(song_names)
    create_artists_table(cur, conn)
    create_tracks_table(cur, conn)
    fill_spotify_tables('spotify_tracks.json', cur, conn)



if __name__ == "__main__":
    main()