import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

import csv
# import boto3
# import pandas as pd
import sys

from datetime import datetime

def configure():
    load_dotenv()

def extract_spotify(num_tracks=15):
    """
    Calls Spotify API using credentials to extract
    most recently played tracks
    INPUT: Takes in spotify API credentials that are defined
    in global variables
    RESULT: returns JSON response
    """
    spotify_client_id = os.getenv('spotify_client_id')
    spotify_client_secret = os.getenv('spotify_client_secret')
    spotify_redirect_url = "http://localhost:3000"
    scope = "user-read-recently-played"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri=spotify_redirect_url,
        scope=scope))

    results = sp.current_user_recently_played(limit = num_tracks)
    return results

def albums(results):
    """
    DOCSTRING: Creates the album datastructure. 
    INPUT: Results - JSON of the responses from Spotify API call
    RESULT: List - a list of strings of album names. 
    """
    albums = []
    for items in results['items']:
        print(items)