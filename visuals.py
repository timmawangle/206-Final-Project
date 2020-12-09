import matplotlib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def bar_graph(cur, conn):
    cur.execute('SELECT track_name FROM tracks_videos')
    temp = cur.fetchall()
    labels = []
    for tup in temp:
        labels.append(tup[0])
    cur.execute('SELECT pop_index FROM tracks_videos')
    temp = cur.fetchall()
    spotify_ranks = []
    for i in range(len(temp)):
        spotify_ranks.append(i+1)
    cur.execute('SELECT ranking FROM tracks_videos')
    temp = cur.fetchall()
    youtube_ranks = []
    for tup in temp:
        youtube_ranks.append(tup[0])

    fig, ax = plt.subplots()

    N = 100
    width = 0.5
    ind = np.arange(N)

    p1 = ax.bar(ind, spotify_ranks, width, color='green')
    p2 = ax.bar(ind + width, youtube_ranks, width, color='red')

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(labels, rotation = 'vertical', fontsize = 2)
    ax.legend((p1[0],p2[0]), ('Spotify', 'Youtube'))
    ax.margins(0.5)
    ax.autoscale_view()

    ax.set(xlabel='Song', ylabel='Ranking',
       title='Spotify and Youtube Top 100 Songs Ranked')

    ax.grid()

    fig.savefig("YT_SPOTIFY_BAR.png")
    plt.show()

def bar_chart(cur, conn):
    cur.execute('SELECT track_name FROM tracks_videos')
    temp = cur.fetchall()
    labels = []
    for tup in temp:
        labels.append(tup[0])
    cur.execute('SELECT pop_index FROM tracks_videos')

    cur.execute('SELECT tracks_videos.track_name, Artists.name, tracks_videos.pop_index, tracks_videos.ranking FROM tracks_videos JOIN Artists ON tracks_videos.artist_id=Artists.artist_id')
    songs = cur.fetchall()
    difference_list = []

    for i in range(len(songs)):
        diff = abs((i + 1) - (songs[i][3]))
        difference_list.append(diff)

    total = 0
    for dif in difference_list:
        total += dif
    
    avg = total / len(difference_list)

    fig, ax = plt.subplots()

    N = 100
    width = 0.5
    ind = np.arange(N)

    p1 = ax.bar(ind, difference_list, width, color='#ffc94a')

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(labels, rotation = 'vertical', fontsize = 2)
    ax.margins(0.5)
    ax.autoscale_view()

    ax.set(xlabel='Song', ylabel='Difference in Ranking',
       title='Spotify and Youtube Top 100 Songs Difference in Ranking')

    ax.grid()

    fig.savefig("difference_ranked_bar.png")
    plt.show()


def main():
    cur, conn = setUpDatabase('top_songs.db')
    bar_graph(cur, conn)
    bar_chart(cur, conn)

if __name__ == "__main__":
    main()
