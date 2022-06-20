import extract
import transform
# import pandas as pd
# from datetime import datetime, timezone

# extract.configure()
# results = extract.extract_spotify()
# print(extract.albums(results))
# print(extract.artists(results))
# print(extract.tracks(results)) 

# Test whether the dataframes were created successfully
#albumsdf = transform.AlbumsDataFrame(extract.albums(results))
#print(albumsdf)
# artistsdf = transform.ArtistsDataFrame(extract.artists(results))
# tracksdf = transform.TracksDataFrame(extract.tracks(results))
# print(albumsdf['AlbumReleaseDate'])

## testing datetime on TrackTimePlayed
#print(tracksdf['TrackTimePlayed'])
#tracksdf['TrackTimePlayed'] = pd.to_datetime(tracksdf['TrackTimePlayed'])
#print(tracksdf['TrackTimePlayed'])
# print(tracksdf['TrackTimePlayed'].dt.tz_convert('US/Pacific'))
#tracksdf['TrackTimePlayed'] = tracksdf['TrackTimePlayed'].dt.tz_convert('US/Pacific')
# ATTEMPT 1 ------------------------------------------------------------------
# tracksdf['TrackTimePlayed'] = tracksdf['TrackTimePlayed'].astype(str).str[:-7]
# print(tracksdf['TrackTimePlayed'])
# tracksdf['TrackTimePlayed'] = pd.to_datetime(tracksdf['TrackTimePlayed'])
# print(tracksdf['TrackTimePlayed']),
# ATTEMPT 2 ------------------------------------------------------------------
#tracksdf['TrackTimePlayed'] = tracksdf['TrackTimePlayed'].dt.tz_convert(None)
#print(tracksdf['TrackTimePlayed'])

## testing dtypes of each dataframe
# albumsdf.info()
# artistsdf.info()
# tracksdf.info()

# TEST: Debugging entire transform
extract.configure()
results = extract.extract_spotify()
albums = extract.albums(results)
tracks = extract.tracks(results)
artists = extract.artists(results)

tracksdf, albumsdf, artistsdf = transform.transform(tracks, albums, artists)
print(albumsdf)


## TEST: Debugging transform function by only looking at albums
# extract.configure()
# results = extract.extract_spotify()
# albums = extract.albums(results)
# albumsdf = transform.transform(albums, albums, albums)
# print(albumsdf)