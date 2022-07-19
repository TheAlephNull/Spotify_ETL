import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import psycopg2.extras as extras
from sqlalchemy import create_engine
import sys
import pandas as pd
from datetime import date
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

def create_csv(tracksdf, albumsdf, artistsdf):
    """
    DOCSTRING: Converts tracks, albums, and artists dataframes into 3 csv files
    INPUTS: tracksdf (Pandas DataFrame), albumsdf( Pandas DataFrame), artistsdf 
    (Pandas DataFrame) - after transformation done in `transform.py`
    RETURNS: tracks, albums, artists.csv (CSV) - in downloads folder
    """
    today = date.today()
    tracksdf.to_csv(f"C:/Users/henrya1/Downloads/tracks{today}.csv")
    albumsdf.to_csv(f"C:/Users/henrya1/Downloads/albums{today}.csv")
    artistsdf.to_csv(f"C:/Users/henrya1/Downloads/artists{today}.csv")

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
    
def setup_psql(dbname = ""):
    """To create database"""
    postgres_password = os.getenv('postgres_password')
    user = os.getenv('user')
    host='localhost'

    if dbname == "":
        postgres_password = os.getenv('postgres_password')
        
        conn_params_dic = {
            "host": host,
            "user": user,
            "password": postgres_password
        }
    else:
        conn_params_dic = {
            "host": host,
            "database": dbname,
            "user": user,
            "password": postgres_password,
        }

    return conn_params_dic # 1

def connect(conn_params_dic):
    conn = None
    try:
        print('Connecting to PostgreSQL')
        conn = psycopg2.connect(**conn_params_dic) # 2
        conn.autocommit = True
        print('Connection successful..................')
    
    except OperationalError as err:
        show_psycopg2_exception(err)
        conn = None # set to none in case of error
    return conn

def create_db(conn, dbname='table'):
    if conn != None:
        try: 
            cursor = conn.cursor() # 3
            cursor.execute(f"DROP DATABASE IF EXISTS {dbname};") # drop table if exists
            cursor.execute(f"CREATE DATABASE {dbname};")
            print(f"{dbname} database created successfully..................")
            # close cursor and connection
            cursor.close()
            #conn.close() # commented out since next function `create_table` also closes
        except OperationalError as err:
            show_psycopg2_exception(err)
            conn = None

def create_table(tablename, sql_file, conn):
    """
    DOCSTRING: creates a table in psql database based on 
    connection provided using the SQL file to create the
    schema.
    INPUTS: tablename (STRING) - used to name the table,
    sql_file (.sql) - sql code to create schema
    conn (Database Connection) - connection to psql 
    using parameters
    """
    fd = open(sql_file,'r')
    sql = fd.read()

    if conn != None:
        try:
            cursor = conn.cursor()
            # drop table if exists
            cursor.execute(sql)
            print(f'{tablename} table created successfully.............')
            cursor.close()
            # conn.close() # conn.close() will be called only once outside of function
        except OperationalError as err:
            show_psycopg2_exception(err)
            conn = None

def joinsql(table, cols):
    """HELPER FUNCTION: returns sql code thats needed"""
    if table == 'tracks':
        sql = "INSERT INTO %s (%s) VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)" % (table, cols)
    elif table == 'albums':
        sql = "INSERT INTO %s (%s) VALUES (%%s, %%s, %%s, %%s, %%s, %%s)" % (table, cols)
    elif table == 'artists':
        sql = "INSERT INTO %s (%s) VALUES (%%s, %%s, %%s)" % (table, cols)
    return sql
        
# Define function using cursor.executemany() to insert the dataframe
def execute_many(conn, df, table):
    # Creating a list of tupples from the dataframe values
    tpls = [tuple(x) for x in df.to_numpy()]
    # dataframe columns with Comma-separated
    cols = ','.join(list(df.columns))
    # SQL query to execute
    sql = joinsql(table, cols)
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, tpls)
        conn.commit()
        print(f"Data inserted in {table} using execute_many() successfully...")
    except (Exception, psycopg2.DatabaseError) as err:
        # pass exception to function
        show_psycopg2_exception(err)
        cursor.close()