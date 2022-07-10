#! /home/guido/miniconda3/envs/spotify/bin/python

import config as cfg

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_connection():
    spotify = cfg.spotify
    auth = SpotifyOAuth(
        client_id = spotify["client_id"],
        client_secret = spotify["client_secret"],
        redirect_uri = spotify["redirect_uri"],
        scope="user-read-recently-played",
        open_browser=False)
    sp = spotipy.Spotify(auth_manager=auth)
    return sp

def get_token(sp):
    try:
        sp.auth_manager.get_access_token(as_dict=True)
        print('token obtenido')
    except:
        print('error')