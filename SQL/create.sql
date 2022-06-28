-- to create tables

-- Tracks
CREATE TABLE IF NOT EXISTS tracks (
    SpotifyTrackID TEXT PRIMARY KEY NOT NULL,
    TrackName TEXT NOT NULL,
    TrackURL TEXT,
    TrackPopularity SMALLINT,
    TrackTimePlayed DATETIME2,
    TrackDuration INTEGER,
    ArtistID TEXT,
    AlbumID TEXT
);

-- Albums
CREATE TABLE IF NOT EXISTS albums (
    AlbumID TEXT PRIMARY KEY NOT NULL,
    AlbumName TEXT NOT NULL,
    NumTracks SMALLINT,
    AlbumReleaseDate DATETIME2,
    AlbumURL TEXT,
    AlbumType TEXT
);

-- Artists
CRETE TABLE IF NOT EXISTS artists (
    ArtistID TEXT PRIMARY KEY NOT NULL,
    ArtistName TEXT NOT NULL,
    ArtistURL TEXT
);
