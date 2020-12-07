import json
import unittest
import os
import requests
import sqlite3

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Names
# Timothy Wang - timwa@umich.edu
# Emily Choe - emchoe@umich.edu

#YouTube API Info
API_KEY = 'AIzaSyD2NJk0i7N6SLl1SHzr1sOeMUuaDkcxRJ0'
Y_CLIENT_ID = '517531547391-96erielcd69ssc725h23vv6mhnv86d84.apps.googleusercontent.com'
Y_CLIENT_SECRET = 'sq9j0OQYjbgMH9mIkst-7q8O'
#Youtube
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def write_json(youtube_json, youtube_dict):
    filepath = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(filepath, youtube_json)

    dumped = json.dumps(youtube_dict, indent=4, sort_keys=True)
    fw = open(file, 'w')
    fw.write(dumped)
    fw.close()

def get_youtube_json():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    filepath = os.path.dirname(os.path.realpath(__file__))
    client_secrets_file = os.path.join(filepath, client_secrets_file)

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=100,
        playlistId="PLDIoUOhQQPlXr63I_vwF9GD8sAKh77dWU"
    )

    response_page1 = request.execute()
    videos = response_page1['items']
    
    #video_list.append(response)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=100,
        pageToken="CDIQAA",
        playlistId="PLDIoUOhQQPlXr63I_vwF9GD8sAKh77dWU"
    )
    response_page2 = request.execute()
    videos += response_page2['items']

    write_json('youtube_tracks.json', videos)


def main():
    get_youtube_json()

if __name__ == "__main__":
    main()
