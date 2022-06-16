import csv
import boto3
import pandas as pd
import sys
 
from datetime import datetime, timezone

import extract

# variables imported:
# artists: List of Dictionaries
# albums: List of Dictionaries
# tracks: Dictionaries of Lists
# albums = []
# artists = []
# tracks = {}

def clean(df):
    """
    DOCSTRING: Removes duplicates and checks for nulls
    INPUTS: df (Pandas DataFrame) - the output of transforming
    the reponse from 'extract.py'
    RETURNS: cleaned (Pandas DataFrame)
    """
    # To-Do:
    # 1. Remove duplicates
    # 2. Remove nulls if any
    df.drop_duplicates() # 1

    numNulls = pd.isnull(df).values.sum() 
    if numNulls == 0: # 2
        print("No nulls found! All clean")
    else:
        print(f"""
        Number of Nulls found: {numNulls}
        Please review the data before proceeding!
        """)
    
    return df

def AlbumsDataFrame(albums):
    """
    DOCSTRING: Creates a Pandas DataFrame of the albums 
    data structure & cleans
    INPUTS: albums (List of Dictionaries)
    RETURNS: DataFrame
    """
    albums_df = pd.DataFrame.from_dict(albums) # make DataFrame
    clean(albums_df) # clean data
    return albums_df

def TracksDataFrame(tracks):
    """
    DOCSTRING: Creates Pandas DataFrame of the tracks 
    data structure & cleans
    INPUTS: tracks (List of Dictionaries)
    RETURNS: DataFrame
    """
    tracks_df = pd.DataFrame.from_dict(tracks)
    clean(tracks_df)
    return tracks_df
    
def ArtistsDataFrame(artists):
    """
    DOCSTRING: Creates Pandas DataFrame of the artists 
    data structure & cleans
    INPUTS: artists (Dictionary of Lists)
    RETURNS: artists_df (Pandas DataFrame)
    """
    artists_df = pd.DataFrame(artists)
    clean(artists_df)
    return artists_df

def transform_date(df, toDate, zone='US/Pacific'):
    """
    DOCSTRING: (HELPER FUNCTION) Transforms tracks_df[toDate] to 
    approrpiate DateTime object without the timezone stamp for 
    SQL compatibility
    INPUT: df (Pandas DataFrame) - of data structure, 
    toDate (list) - list of columns that need to be fixed
    timezone (string) - preferred time zone for conversion before UNIX
    RETURNS: tracks_df[toDate]
    """
    df_copy = df.copy()
    # for column in list provided: change to datetime
    df_copy[toDate] = df_copy[toDate].apply(pd.to_datetime)
    # change to local time zone by indexing first element of toDate 
    # (since only one element)
    df_copy[toDate[0]] = df_copy[toDate[0]].dt.tz_convert(zone)
    # remove time zone portion form DateTime object (not supported in SQL)
    df_copy['TrackTimePlayed'] = df_copy['TrackTimePlayed'].dt.tz_convert(None)

    return df_copy[toDate]

def transform_albums(albums_df):
    """
    DOCSTRING: Takes dataframe and transforms necessary 
    columns to preferred format
    INPUT: df (Pandas DataFrame) 
    RETURNS: albums_df (Pandas DataFrame)
    """
    toString = ['AlbumID','AlbumName','AlbumURL','AlbumType']
    toDate = ['AlbumReleaseDate']

    # change specified columns to string
    albums_df[toString] = albums_df[toString].astype(str)
    # for column in list provided: change to datetime
    albums_df[toDate] = transform_date(albums_df, toDate, 'US/Pacific')

    return albums_df

def create_uniqueID(tracks_df):
    """
    DOCSTRING: (HELPER FUNCTION) Creates a unique identifier for each song 
    in the track DataFrame to ensure that no one song is played twice 
    at the same time. Combines UNIX timestamp of TrackTimePlayed 
    (from datetime) plus SpotifyTrackID
    INPUTS: tracks_df (Pandas DataFrame) - of all song lists extracted
    RETURNS: tracks_df['UniqueID']
    """
    # convert column to unix 
    tracks_copy = tracks_df.copy()
    tracks_copy['UNIXTimestamp'] = tracks_copy['TrackTimePlayed'].dt.timestamp()
    tracks_copy['UNIXTimestamp'] = tracks_copy['UNIX Timestamp'].astype(str)

    # create Unique ID
    tracks_copy['UniqueID'] = tracks_copy['SpotifyTrackID'] + "-" + tracks_copy['UNIXTimestamp']

    return tracks_copy['UniqueID']

def transform_tracks(tracks_df):
    """
    DOCSTRING: Takes dataframe and transforms necessary 
    columns to preferred format. Also, original extracted
    date format is: "2022-06-15T20:41:47.672Z"
    INPUT: df (Pandas DataFrame) 
    RETURNS: albums_df (Pandas DataFrame)
    """
    toString = ['SpotifyTrackID','TrackName','TrackURL','ArtistID','AlbumID']
    toDate = ['TrackTimePlayed']

    # change specified columns to string
    tracks_df[toString] = tracks_df[toString].astype(str)
    # change date columns to dates without timezones
    tracks_df[toDate] = transform_date(tracks_df, toDate, 'US/Pacific')
    # create unique identifier based on song number and time played
    tracks_df['UniqueID'] = create_uniqueID(tracks_df)
    # make UniqueID as first column
    UniqueID = tracks_df.pop('UniqueID')
    tracks_df.insert(0, 'UniqueID', UniqueID)

    return tracks_df

def transform_artists(artists_df):
    """
    DOCSTRING: Takes dataframe and makes necessary 
    changes to the data. In this case, converting data type
    to strings
    INPUTS: artists_df (Pandas DataFrame) - from spotify extraction
    RETURNS: artists_df (Pandas DataFrame)
    """
    toString = ['ArtistID','ArtistName','ArtistURL']
    artists_df[toString] = artists_df[toString].astype(str)

    return artists_df

def transform(tracks_df, albums_df, artists_df):
    """
    DOCSTRING:
    INPUTS:
    RETURNS:
    """
    pass

# Notes:
# error with numpy and mkl-service solved using https://github.com/ThilinaRajapakse/simpletransformers/issues/322