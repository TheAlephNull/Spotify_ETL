-- Create Albums Table
CREATE TABLE IF NOT EXISTS albums (
    AlbumID TEXT PRIMARY KEY NOT NULL,
    AlbumName TEXT NOT NULL,
    NumTracks SMALLINT,
    AlbumReleaseDate TIMESTAMP,
    AlbumURL TEXT,
    AlbumType TEXT
);