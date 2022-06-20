import psycopg2
from sqlalchemy import create_engine
import sys
import pandas as pd

def create_xlsx(tracksdf, albumsdf, artistsdf):
    """
    DOCSTRING: Converts tracks, albums, and artists dataframes into one excel sheet
    INPUTS: tracksdf (Pandas DataFrame), albumsdf( Pandas DataFrame), artistsdf 
    (Pandas DataFrame) - after transformation done in `transform.py`
    RETURNS: toptracks.xlsx (Excel Sheet) - in downloads folder
    """
    with pd.ExcelWriter("Downloads\toptracks.xlsx") as writer:
        tracksdf.to_excel(writer, sheet_name = 'tracks', index = False)
        albumsdf.to_excel(writer, sheet_name = 'albums', index = False)
        artistsdf.to_excel(writer, sheet_name = 'artists', index = False)
        