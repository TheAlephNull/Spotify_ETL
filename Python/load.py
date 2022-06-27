import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
from sqlalchemy import create_engine
import sys
import pandas as pd
import os

def create_xlsx(tracksdf, albumsdf, artistsdf):
    """
    DOCSTRING: Converts tracks, albums, and artists dataframes into one excel sheet
    INPUTS: tracksdf (Pandas DataFrame), albumsdf( Pandas DataFrame), artistsdf 
    (Pandas DataFrame) - after transformation done in `transform.py`
    RETURNS: toptracks.xlsx (Excel Sheet) - in downloads folder
    """
    with pd.ExcelWriter("C:/Users/henrya1/Downloads/toptracks.xlsx") as writer:
        tracksdf.to_excel(writer, sheet_name = 'tracks', index = False)
        albumsdf.to_excel(writer, sheet_name = 'albums', index = False)
        artistsdf.to_excel(writer, sheet_name = 'artists', index = False)

def show_psycopg2_exception(err):
    """ (HELPER FUNCTION) OBTAINED FROM ARTICLE: """
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occured
    line_n = traceback.tb_lineno
    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)
    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)
    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    
def setup_psql():
    """To create database"""
    postgres_password = os.getenv('postgres_password')
    
    conn_params_dic = {
        "host": "",
        "user": "",
        "password": postgres_password
    }
    return conn_params_dic # 1

def setup_params(name):
    """
    DOCSTRING: After database has been created
    """
    postgres_password = os.getenv('postgres_password')

    conn_params_dic = {
        "host":"",
        "database":name,
        "user":"",
        "password":os.getenv(postgres_password),
    }

    return conn_params_dic

def connect(conn_params_dic):
    conn = None
    try:
        print('Connecting to PostgreSQL')
        conn = psycopg2.connect(**conn_params_dic) # 2
        print('Connection successful..................')
    
    except OperationalError as err:
        show_psycopg2_exception(err)
        conn = None # set to none in case of error
    return conn

def create_db(conn_params_dic, dbname='table'):
    conn = connect(conn_params_dic)
    conn.autocommit = True

    if conn != None:
        try: 
            cursor = conn.cursor() # 3
            cursor.execute(f"DROP DATABASE IF EXISTS {dbname};") # drop table if exists
            cursor.execute(f"CREATE DATABASE {dbname};")
            print(f"{dbname} database created successfully..................")
            # close cursor and connection
            cursor.close()
            conn.close()
        except OperationalError as err:
            show_psycopg2_exception(err)
            conn = None

def create_tracks(dbname, conn):
    """
    """
    if conn != None:
        try:
            cursor = conn.cursor()
            # drop table if exists
            sql = '''CREATE TABLE tracks(
            SpotifyTrackID TEXT PRIMARY KEY NOT NULL,
            TrackName TEXT NOT NULL,
            TrackURL TEXT,
            TrackPopularity SMALLINT,
            TrackTimePlayed DATETIME2,
            TrackDuration INTEGER,
            ArtistID TEXT,
            AlbumID TEXT,
            )'''
        except OperationalError as err:
            show_psycopg2_exception(err)
            conn = None

def postgres_conn(conn_params_dic):
    """
    DOCSTRING: Initiates the connection to postgreSQL
    using SQLAlchemy
    """
    connection = '-postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]'
    