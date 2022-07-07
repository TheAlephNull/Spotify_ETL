import extract as e
import load as l
import transform as t

# Extract
def extract():
    API_results = e.extract_spotify(15)

    albums = extract.albums(API_results)
    tracks = extract.tracks(API_results)
    artists = extract.artists(API_results)

    return tracks, albums, artists

def transform(tracks, albums, artists):
    return t.transform(tracks, albums, artists)

def load(tracks, albums, artists):
    # Convert to csv
    l.create_csv(tracks, albums, artists)
    # IF DATABASE IS NEW:
    try:
        # connect & create db
        l.setup_params('spotify_etl')
    except:# ELSE:
        # connect
        pass
    # load data to databases
    pass

e.configure()