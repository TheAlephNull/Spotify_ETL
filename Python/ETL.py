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
    l.create_db(conn_param_dic, dbname)
    conn_param_dic = l.setup_params(dbname)
    l.create_table('Tracks', 'SQL/tracks.sql', conn_param_dic)
    l.create_table('Albums', 'SQL/albums.sql', conn_param_dic)
    l.create_table('Artists', 'SQL/artists.sql', conn_param_dic)

def load(tracks, albums, artists, dbname):
    """Assumes that database and table have been created"""
    conn_param_dic = l.setup_params(dbname)
    conn = l.connect(conn_param_dic)
    conn.autocommit = True

    l.execute_many(conn, dbname, 'Tracks')
    l.execute_many(conn, dbname, 'Albums')
    l.execute_many(conn, dbname, 'Artists')

if __name__ == "__main__":
    # INPUTS
    numtracks = 15
    dbname = 'SpotifyTMP'
    # ETL'
    e.configure()
    tracks, albums, artists = extract(numtracks) # extract tracks
    print("Successfully extracted from Spotify..............")
    tracks, albums, artists = transform(tracks, albums, artists)
    print("Successfully transformed data.................")
    try:
        print('tried this')
        load(tracks, albums, artists, dbname)
    except:
        print('then i tried this')
        firstload(dbname)
        load(tracks, albums, artists, dbname)

    print("Finished Extract, Load, Transform Spotify")