import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

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
    INPUT: Results (JSON) - the responses from Spotify API call
    RETURNS: albums (a list of dictionaries) - containing album from track 
    """
    albums = []
    for items in results['items']:
        # columns of information I want:
            # 0. Album ID
            # 1. Album Name
            # 2. Total Tracks
            # 3. Album Release Date
            # 4. Album URL
            # 5. Album Type
        album_ID = items['track']['album']['id']
        album_name = items['track']['album']['name']
        total_tracks = items['track']['album']['total_tracks']
        album_release_date = items['track']['album']['release_date']
        album_URL = items['track']['album']['external_urls']['spotify']
        album_type = items['track']['album']['album_type']

        # album dictionary containing necessary info (to append)
        album = {
            'AlbumID': album_ID,
            'AlbumName':album_name,
            'NumTracks':total_tracks,
            'AlbumReleaseDate':album_release_date,
            'AlbumURL':album_URL,
            'AlbumType':album_type
        }

        # add album to our list of albums
        albums.append(album)

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
        Track_URL = items['track']['external_urls']['spotify'] # 3. Track URL
        Track_Popularity = items['track']['popularity'] # 4. Track Popularity (out of 100?)
        Track_Duration = items['track']['duration_ms'] # 5. Track Duration (in ms)
        Track_TimePlayed = items['played_at'] # 6. Track Time Played      
        Artist_ID = items['track']['artists'][0]['id'] # 7. Artist ID
        Album_ID = items['track']['album']['id'] # 8. Album ID

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
    DOCSTRING: Creates the artist data structure
    INPUTS: results (JSON) - response from API call
    RESULT: artists (Dictionary of Lists)
    """
    Artist_ID = []
    Artist_Name = []
    Artist_URL = []
    for items in results['items']:
        for name in items['track']['artists']:
            # columns I want:
            # 1. Spotify Artist ID
            # 2. Artist Name
            # 3. Artist URL
            Artist_ID.append(name['id'])
            Artist_Name.append(name['name'])
            Artist_URL.append(name['external_urls']['spotify'])
    
    artists = {
        'ArtistID':Artist_ID,
        'ArtistName':Artist_Name,
        'ArtistURL':Artist_URL
    }

    return artists