import csv
import boto3
import pandas as pd
import sys
 
from datetime import datetime

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

def transform_albums(albums_df):
    """
    DOCSTRING: Takes dataframe and transforms necessary 
    columns to preferred format
    INPUT: df (Pandas DataFrame) 
    RESULTS: albums_df (Pandas DataFrame)
    """
    toString = ['AlbumID','AlbumName','AlbumURL','AlbumType']
    toDate = ['AlbumReleaseDate']

    # change specified columns to string
    albums_df[toString] = albums_df[toString].astype(str)
    # for column in list provided: change to datetime
    albums_df[toDate] = albums_df[toDate].apply(pd.to_datetime)

    return albums_df

def transform_tracks(tracks_df):
    """
    DOCSTRING: Takes dataframe and transforms necessary 
    columns to preferred format. Also, original extracted
    date format is: "2022-06-15T20:41:47.672Z"
    INPUT: df (Pandas DataFrame) 
    RESULTS: albums_df (Pandas DataFrame)
    """
    toString = ['SpotifyTrackID','TrackName','TrackURL','ArtistID','AlbumID']
    toDate = ['TrackTimePlayed']

    # change specified columns to string
    tracks_df[toString] = tracks_df[toString].astype(str)
    # for column in list provided: change to datetime
    tracks_df[toDate] = tracks_df[toDate].apply(pd.to_datetime)

    return tracks_df
# Notes:
# error with numpy and mkl-service solved using https://github.com/ThilinaRajapakse/simpletransformers/issues/322