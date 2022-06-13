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
        # columns I want:
        # 1. Album Name
        # 2. Total Tracks
        # 3. Album Release Date
        # 4. Album URL
        # 5. Album Type
        album_name = 
        total_tracks = 
        album_release_date = 
        album_URL = 
        album_type = 

        album = {
            'AlbumName':,
            'NumTracks':,
            'AlbumReleaseDate':,
            'AlbumURL':,
            'AlbumType':
        }
    
    return albums

def tracks(results):
    """
    DOCSTRING: Creates the track datastructure.
    INPUTS: API response (JSON)
    RETURNS: tracks (List of Dictionaries) - each entry contains
    the track and track information
    """
    tracks = []

    for items in results['items']:
        # columns of information I want:
        Spotify_TrackID = items['track']['id'] # 1. Spotify Track ID
        Track_Name = items['track']['name'] # 2. Track Name
        Track_URL = items['track']['href'] # 3. Track URL
        Track_Popularity = items['track']['popularity'] # 4. Track Popularity (out of 100?)
        Track_TimePlayed = items['track']['duration_ms'] # 5. Track Duration (in ms)
        Track_Duration = items['played_at'] # 6. Track Time Played      
        Artist_ID = items['artists'][0]['id'] # 7. Artist ID
        Album_ID = items['album']['id'] # 8. Album ID

        # Create dictionary that contains track information
        track = {
            'SpotifyTrackID':Spotify_TrackID,
            'TrackName':Track_Name,
            'TrackURL':Track_URL,
            'TrackPopularity':Track_Popularity,
            'TrackTimePlayed':Track_TimePlayed,
            'TrackDuration':Track_Duration,
            'ArtistID':Artist_ID,
            'AlbumID':Album_ID
            }
        
        # add track to list of tracks
        tracks.append(track)

    return tracks


def artists(results):
    """
    DOCSTRING:
    INPUTS:
    RESULT:
    """
    for items in results['items']:
        # columns I want:
        # 1. Spotify Artist ID
        # 2. Artist ID?
        # 3. Artist Name
        pass