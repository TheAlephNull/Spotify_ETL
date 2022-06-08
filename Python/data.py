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

def setup_etl(num_tracks=15):
    """
    Calls Spotify API using credentials to extract
    most recently played tracks
    INPUT: Takes in spotify API credentials that are defined
    in global variables
    RESULT: prints JSON response
    """
    spotify_client_id = os.getenv('spotify_client_id')
    spotify_client_secret = os.getenv('spotify_client_secret')
    spotify_redirect_url = "http://localhost"
    scope = "user-read-recently-played"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_recently_played(int = num_tracks)
    print(results)