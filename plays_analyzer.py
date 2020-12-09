import json
import unittest
import os
import requests
import sqlite3
import spotipy
import spotipy.util as util
import re

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
    #count = 0

    for song in song_names:
        r = requests.get(BASE_URL + song + '&type=track&market=US&limit=1', headers=headers)
        results = json.loads(r.text)
        tracks_list.append(results)
        write_json('spotify_tracks.json', tracks_list)
        #r = r.json()
        #write_json('spotify_tracks.json', r)
        #tracks_dict[song] = r
        #if count < 25:
            #count += 1
        #else:
            #break
    return tracks_list


#def add_artists(cur, conn, index, name):
    #cur.execute("INSERT INTO Artists(artist_id, name) VALUES (?,?)", (index, name))
    #conn.commit()


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
        #print(count)
        name = track['tracks']['items'][0]['name']
        artist = track['tracks']['items'][0]['artists'][0]['name']
        popularity_num = track['tracks']['items'][0]['popularity']
        #print(popularity_num)
        if artist not in unique_artists:
            unique_artists.append(artist)

        temp = (name, artist, popularity_num)
        #print(temp)
        tracks_list.append(temp)

    #artist_ids = {}
    #count = 0
    #for artist in unique_artists:
        #add_artists(cur, conn, count, artist)
        #artist_ids[artist] = count
        #count += 1
    artist_ids = add_artists(cur, conn, unique_artists)
    #print(artist_ids)
    add_tracks(cur, conn, tracks_list, artist_ids)
    #count = 0
    #for track in tracks_list:
        #add_tracks(cur, conn, count, track[0], artist_ids[track[1]], track[2])
        #count += 1


def create_artists_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Artists (artist_id INTEGER, name TEXT)")
    conn.commit()


def create_tracks_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Tracks (track_id INTEGER, track_name TEXT, artist_id INTEGER, pop_index INTEGER)")
    conn.commit()


#def add_tracks(cur, conn, track_index, track_name, artist_index, popularity_index):
    #cur.execute("INSERT INTO Tracks(track_id, track_name, artist_id, pop_index) VALUES (?,?,?,?)", (track_index, track_name, artist_index, popularity_index))
    #conn.commit()

def add_artists(cur, conn, artists):
    #print(len(artists))
    cur.execute('SELECT name FROM Artists')
    inserted_artists = cur.fetchall()
    num_artists = len(inserted_artists)
    max_artists = num_artists + 25
    cur.execute('SELECT name, artist_id FROM Artists')
    #print('AL:KSHDLASDKASD:ASKJDas')
    artist_ids = {}
    pairs = cur.fetchall()
    for pair in pairs:
        artist_ids[pair[0]] = pair[1]
    #print(artist_ids)
    
    if num_artists >= len(artists):
        return artist_ids
    if max_artists >= len(artists):
        max_artists = len(artists)

    count = num_artists
    for artist in artists:
        #print(count)
        #print(max_artists)
        if count < max_artists:
            if artist not in inserted_artists:
                cur.execute("INSERT INTO Artists(artist_id, name) VALUES (?,?)", (count, artists[count]))
                artist_ids[artists[count]] = count
                count += 1
            else:
                continue
        else:
            break
    
    
    #while num_artists < (max_artists or len(artists)):
        #print(num_artists)
        #print(artists[num_artists])
        #cur.execute("INSERT INTO Artists(artist_id, name) VALUES (?,?)", (num_artists, artists[num_artists]))
        #artist_ids[artists[num_artists]] = num_artists
        #num_artists += 1

    conn.commit()
    #print(artist_ids)
    return artist_ids

def add_tracks(cur, conn, track_list, artist_ids):
    #print(artist_ids)

    cur.execute('SELECT track_name FROM Tracks')
    inserted_songs =  cur.fetchall()
    num_songs = len(inserted_songs)
    max_songs = num_songs + 25

    if num_songs >= 100:
        return

    while num_songs < max_songs:
        #print(num_songs)
        #print(track_list[num_songs][0])
        cur.execute("INSERT INTO Tracks(track_id, track_name, artist_id, pop_index) VALUES (?,?,?,?)", (num_songs, track_list[num_songs][0], artist_ids[track_list[num_songs][1]], track_list[num_songs][2]))
        num_songs += 1
    conn.commit()


def get_playlist_info(filename, cur, conn):
    filepath = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(filepath, filename)
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)

    video_list = []

    # Table | video_id | video_name | video_ranking |
    for video in json_data:
        position = video['snippet']['position']
        title = video['snippet']['title']

        #Filter from video title main artist name, track name, and ranking
        title = title.split('(O')[0]
        title = title.split('(o')[0]
        title = title.split('[O')[0]
        if '-' in title:
            artist = title.split('-')[0].strip()
            title = title.split('-')[1].strip()
        if '–' in title:
            artist = title.split('–')[0].strip()
            title = title.split('–')[1].strip()
        if re.search("'.+'", title):
            artist = title.split("'")[0].split('(')[0].strip()
            title = title.split("'")[1].strip()
        if re.search('".+"', title):
            artist = title.split('"')[0].strip()
            title = title.split('"')[1].strip()
        title = title.split('(')[0].strip()
        title = title.split(' ft')[0].strip()
        title = title.split(' feat')[0].strip()
        title = title.split(' Featuring')[0].strip()
        title = title.split(' FT')[0].strip()

        artist = artist.split(' feat.')[0].strip()
        artist = artist.split(',')[0].strip()
        artist = artist.split(' x ')[0].strip()
        artist = artist.split(' ft.')[0].strip()

        title = title.lstrip()
        title = title.strip()

        #print("artist: " + artist)
        #print('title: ' + title)
        #print('position: ' + str(position))
        #print(' ')

        temp = (artist, title, position + 1)
        video_list.append(temp)

    return video_list

def create_video_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Videos (video_id INTEGER, video_name TEXT, artist_name TEXT, ranking INTEGER)")
    conn.commit()

def add_videos_db(cur, conn, video_list):
    #video_list = [(artist, title, position),...]
    cur.execute('SELECT video_name FROM Videos')
    inserted_videos =  cur.fetchall()
    num_videos = len(inserted_videos)
    max_videos = num_videos + 25

    if num_videos == 100:
        return

    while num_videos < max_videos:
        cur.execute("INSERT INTO Videos(video_id, video_name, artist_name, ranking) VALUES (?,?,?,?)", (num_videos, video_list[num_videos][1], video_list[num_videos][0], video_list[num_videos][2]))
        num_videos += 1
    conn.commit()


def get_video_list(video_tuples):
    titles = []
    for tup in video_tuples:
        titles.append(tup[1])
    #print(titles)
    return titles

def join_tables(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS tracks_videos as SELECT Tracks.track_name, Tracks.artist_id, Tracks.pop_index, Videos.ranking FROM Tracks JOIN Videos ON Tracks.track_id=Videos.video_id ORDER BY pop_index DESC')
    cur.execute('SELECT tracks_videos.track_name, Artists.name, tracks_videos.pop_index, tracks_videos.ranking FROM tracks_videos JOIN Artists ON tracks_videos.artist_id=Artists.artist_id')
    songs = cur.fetchall()
    #print(songs)
    difference_list = []
    filepath = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(filepath, "calculations.txt")
    
    f = open(filename, "w")

    for i in range(len(songs)):
        f.write("Spotify's ranking of " + str(songs[i][0]) + " by " + str(songs[i][1]) + " is " + str(i + 1) + ". \n")
        f.write("Youtube's ranking of " + str(songs[i][0]) + " by " + str(songs[i][1]) + " is " + str(songs[i][3]) + ". \n")
        diff = abs((i + 1) - (songs[i][3]))
        f.write("The difference in ranking is " + str(diff) + ". \n")
        f.write("\n")
        difference_list.append(diff)

    total = 0
    for dif in difference_list:
        total += dif
    
    #print(len(difference_list))
    avg = total / len(difference_list)

    f.write("The average difference between Youtube and Spotify's ranking is " + str(avg))
    f.close()

def main():
    cur, conn = setUpDatabase('top_songs.db')
    videos = get_playlist_info('youtube_tracks.json', cur, conn)
    create_video_table(cur, conn)
    add_videos_db(cur, conn, videos)
    find_song_ids(get_video_list(videos))
    create_artists_table(cur, conn)
    create_tracks_table(cur, conn)
    fill_spotify_tables('spotify_tracks.json', cur, conn)
    join_tables(cur, conn)


if __name__ == "__main__":
    main()