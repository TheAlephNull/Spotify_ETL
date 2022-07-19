-- Tracks
CREATE TABLE IF NOT EXISTS tracks (
    UniqueID TEXT PRIMARY KEY NOT NULL,
    SpotifyTrackID TEXT NOT NULL,
    TrackName TEXT NOT NULL,
    TrackURL TEXT,
    TrackPopularity SMALLINT,
    TrackTimePlayed TIMESTAMP,
    TrackDuration INTEGER,
    ArtistID TEXT,
    AlbumID TEXT
);