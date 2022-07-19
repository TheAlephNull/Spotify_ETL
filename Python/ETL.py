import extract as e
import load as l
import transform as t

# Extract
def extract(num_tracks):
    API_results = e.extract_spotify(num_tracks)

    albums = e.albums(API_results)
    tracks = e.tracks(API_results)
    artists = e.artists(API_results)

    return tracks, albums, artists

def transform(tracks, albums, artists):
    return t.transform(tracks, albums, artists)

def firstload(dbname):
    """:/"""
    # Create TEMP database & table to house data
    conn_param_dic = l.setup_psql()
    conn = l.connect(conn_param_dic)
    l.create_db(conn, dbname)
    conn.close()
    # reestablish connection since parameters updated
    conn_param_dic = l.setup_psql(dbname)
    conn = l.connect(conn_param_dic)

    l.create_table('tracks', 'SQL/tracks.sql', conn)
    l.create_table('albums', 'SQL/albums.sql', conn)
    l.create_table('artists', 'SQL/artists.sql', conn)
    # conn.close()
    print('`tracks`, `albums`, and `artists` tables created successfully...............')

def load(tracks, albums, artists, dbname):
    """Assumes that database and table have been created"""
    conn_param_dic = l.setup_params(dbname)
    conn = l.connect(conn_param_dic)

    l.execute_many(conn, tracks, 'tracks')
    l.execute_many(conn, albums, 'albums')
    l.execute_many(conn, artists, 'artists')
    
    conn.close()

if __name__ == "__main__":
    # INPUTS ========================================
    numtracks = 15
    dbname = 'spotifytmp'
    # ETL ===========================================
    # EXTRACT
    e.configure()
    tracks, albums, artists = extract(numtracks) # extract tracks
    print("Successfully extracted from Spotify..............")
    # TRANFORM
    tracks, albums, artists = transform(tracks, albums, artists)
    print("Successfully transformed data.................")
    # LOAD
    try:
        load(tracks, albums, artists, dbname)
    except:
        print(f'{dbname} database does not exist. \nCreating Database....................')
        firstload(dbname)
        load(tracks, albums, artists, dbname)
    print("=========================================")
    print("Finished Extract, Load, Transform Spotify")
    print("=========================================")