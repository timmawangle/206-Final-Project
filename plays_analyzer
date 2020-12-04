import json
import unittest
import os
import requests
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Names
# Timothy Wang - timwa@umich.edu
# Emily Choe - emchoe@umich.edu

#Spotipy API Info
client_id = '9445bfc4e61f43ed83ec2782d464e42c'
client_secret = 'f7fb2a1c147744d1ade617f598eabc46'

#export SPOTIPY_CLIENT_ID='9445bfc4e61f43ed83ec2782d464e42c'
#export SPOTIPY_CLIENT_SECRET='f7fb2a1c147744d1ade617f598eabc46'

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

URI = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'

album = sp.album_tracks(URI)
print(album)

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

