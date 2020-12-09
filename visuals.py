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
    cur.execute('SELECT track_id FROM tracks_videos')
    temp = cur.fetchmany(10)
    labels = []
    for tup in temp:
        labels.append(tup[0])
    cur.execute('SELECT pop_index FROM tracks_videos')
    temp = cur.fetchmany(10)
    spotify_ranks = []
    for i in range(len(temp)):
        spotify_ranks.append(abs((i + 1) - 101))

    cur.execute('SELECT ranking FROM tracks_videos')
    temp = cur.fetchmany(10)
    youtube_ranks = []
    for tup in temp:
        youtube_ranks.append(abs(tup[0] -101))

    fig, ax = plt.subplots()

    N = 10
    width = 0.35
    ind = np.arange(N)

    p1 = ax.bar(ind, spotify_ranks, width, color='#1be329')
    p2 = ax.bar(ind + width, youtube_ranks, width, color='red')

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(labels, rotation = 'horizontal', fontsize = 12)
    ax.legend((p1[0],p2[0]), ('Spotify', 'Youtube'))
    ax.margins(0)
    ax.autoscale_view()

    ax.set(xlabel='Song ID', ylabel='Ranking (100 = Most Popular, 1 = Least Popular)',
       title='Top 10 Spotify Song Rankings vs Corresponding Youtube Rankings')

    ax.grid()

    fig.savefig("YT_SPOTIFY_BAR.png")
    plt.show()

def bar_chart(cur, conn):
    cur.execute('SELECT track_id FROM tracks_videos')
    temp = cur.fetchmany(50)
    labels = []
    for tup in temp:
        labels.append(tup[0])
    cur.execute('SELECT pop_index FROM tracks_videos')

    cur.execute('SELECT tracks_videos.track_name, Artists.name, tracks_videos.pop_index, tracks_videos.ranking FROM tracks_videos JOIN Artists ON tracks_videos.artist_id=Artists.artist_id')
    songs = cur.fetchmany(50)
    difference_list = []

    for i in range(len(songs)):
        diff = abs((i + 1) - (songs[i][3]))
        difference_list.append(diff)

    total = 0
    for dif in difference_list:
        total += dif
    
    avg = total / len(difference_list)

    fig, ax = plt.subplots()

    N = 50
    width = 1
    ind = np.arange(N)

    p1 = ax.bar(ind, difference_list, width, color='#ffc94a')

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(labels, rotation = 'vertical', fontsize = 7)
    ax.margins(0)
    ax.autoscale_view()

    ax.set(xlabel='Song ID', ylabel='Difference in Ranking',
       title='Spotify and Youtube Top 50 Songs Difference in Ranking')

    ax.grid()

    fig.savefig("RANKED_DIFF_BAR.png")
    plt.show()


def main():
    cur, conn = setUpDatabase('top_songs.db')
    bar_graph(cur, conn)
    bar_chart(cur, conn)

if __name__ == "__main__":
    main()
