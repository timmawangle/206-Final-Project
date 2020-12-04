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

#export SPOTIPY_CLIENT_ID='9445bfc4e61f43ed83ec2782d464e42c'
#export SPOTIPY_CLIENT_SECRET='f7fb2a1c147744d1ade617f598eabc46'

#auth_manager = SpotifyClientCredentials()
#sp = spotipy.Spotify(auth_manager=auth_manager)

#token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
#cache_token = token.get_access_token()
#sp = spotipy.Spotify(cache_token)

#URI = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'

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

BASE_URL = 'https://api.spotify.com/v1/'
playlist_id = '37i9dQZF1DXcBWIGoYBM5M'
r = requests.get(BASE_URL + 'albums/' + playlist_id + '/tracks', headers=headers)
print(r)

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

