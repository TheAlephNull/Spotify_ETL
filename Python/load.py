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
albums = []
artists = []
tracks = {}

def AlbumDataFrame(albums):
    """
    DOCSTRING: Creates a Pandas DataFrame of the albums data structure & Cleans
    INPUTS: albums (List of Dictionaries)
    RETURNS: DataFrame
    """
    album_df = pd.from_dict(albums)

    # to clean:
    # remove duplicates
    # remove nulls

# Notes:
# error with numpy and mkl-service solved using https://github.com/ThilinaRajapakse/simpletransformers/issues/322