import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

import csv
import boto3
import pandas as pd
import sys

from datetime import datetime

def configure():
    load_dotenv()

def setup_etl():
    """call api key using os.get('api_key')"""
    spotify_client_id = os.get('spotify_client_id')
    spotify_client_secret = os.get('spotify_client_secret')
    spotify_redirect_url = "http://localhost"
    scope = "user-read-recently-played"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_recently_played(int = 15)
    print(results)