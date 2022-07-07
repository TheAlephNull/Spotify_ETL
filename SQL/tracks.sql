-- Tracks
CREATE TABLE IF NOT EXISTS tracks (
    SpotifyTrackID TEXT PRIMARY KEY NOT NULL,
    TrackName TEXT NOT NULL,
    TrackURL TEXT,
    TrackPopularity SMALLINT,
    TrackTimePlayed TIMESTAMP,
    TrackDuration INTEGER,
    ArtistID TEXT,
    AlbumID TEXT
);