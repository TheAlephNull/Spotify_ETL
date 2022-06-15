import extract
import transform
import pandas as pd

extract.configure()
results = extract.extract_spotify()
# print(extract.albums(results))
# print(extract.artists(results))
# print(extract.tracks(results)) 

# Test whether the dataframes were created successfully
albumsdf = transform.AlbumsDataFrame(extract.albums(results))
artistsdf = transform.ArtistsDataFrame(extract.artists(results))
tracksdf = transform.TracksDataFrame(extract.tracks(results))
#print(albumsdf['AlbumReleaseDate'])
print(tracksdf['TrackTimePlayed'])
print(pd.to_datetime(tracksdf['TrackTimePlayed'])).tz_convert('US/Pacific')

albumsdf.info()
artistsdf.info()
tracksdf.info()