#! /home/guido/miniconda3/envs/spotify/bin/python

import config as cfg
from spotify_connection import get_connection
from utils import *

import json

from datetime import datetime, date, timedelta

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_played_songs(sp, start_date):
    today = datetime(
            date.today().year,
            date.today().month,
            date.today().day
            )
    
    full_songs = []
    delta_date = start_date
    while delta_date <= today:
        delta_timestamp = int(datetime.timestamp(delta_date))
        
        data = sp.current_user_recently_played(
                            limit = 50,
                            after = delta_timestamp
        )

        songs = map(
                    lambda song: {
                        "played_at": song["played_at"],
                        "id": song["track"]["id"],
                        "name": song["track"]["name"],
                        "artists": get_artist_names(
                                        song["track"]["artists"]
                                                    ),
                        "duration_ms": song["track"]["duration_ms"],
                        "popularity": song["track"]["popularity"]
                                },
                    data["items"]
        )

        songs = filter(lambda x: x not in full_songs, songs)
        songs = filter(
            lambda x: to_datetime(x["played_at"]).day == delta_date.day,
            songs
        )
        full_songs.extend(songs)

        delta_date += timedelta(hours=2)

    return full_songs

def pipeline_plays():
    start_date = date.today() - timedelta(weeks=4)
    start_date = datetime.combine(start_date, datetime.min.time())

    sp = get_connection()
    all_tracks = get_played_songs(sp, start_date)
    full_tracks = get_song_features(all_tracks, sp)
    return full_tracks

tracks = pipeline_plays()
for track in tracks:
    print(json.dumps(track))
