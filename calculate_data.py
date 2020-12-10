import json
import unittest
import os
import requests
import sqlite3
import spotipy
import spotipy.util as util
import re

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def join_tables(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS tracks_videos as SELECT Tracks.track_id, Tracks.track_name, Tracks.artist_id, Tracks.pop_index, Videos.ranking FROM Tracks JOIN Videos ON Tracks.track_id=Videos.video_id ORDER BY pop_index DESC')
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
    join_tables(cur, conn)

if __name__ == "__main__":
    main()