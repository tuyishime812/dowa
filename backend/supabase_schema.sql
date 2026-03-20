-- DGT-SOUNDS Database Schema
-- Run this SQL in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create artists table
CREATE TABLE IF NOT EXISTS artists (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create albums table
CREATE TABLE IF NOT EXISTS albums (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id BIGSERIAL REFERENCES artists(id) ON DELETE CASCADE,
    release_year INTEGER,
    cover_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create tracks table
CREATE TABLE IF NOT EXISTS tracks (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    album VARCHAR(255),
    genre VARCHAR(100),
    duration INTEGER DEFAULT 0,
    file_url VARCHAR(500) NOT NULL,
    cover_url VARCHAR(500),
    plays INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create function to increment plays
CREATE OR REPLACE FUNCTION increment_plays(track_id BIGINT)
RETURNS VOID AS $$
BEGIN
    UPDATE tracks
    SET plays = plays + 1
    WHERE id = track_id;
END;
$$ LANGUAGE plpgsql;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tracks_genre ON tracks(genre);
CREATE INDEX IF NOT EXISTS idx_tracks_artist ON tracks(artist);
CREATE INDEX IF NOT EXISTS idx_tracks_created_at ON tracks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tracks_plays ON tracks(plays DESC);
CREATE INDEX IF NOT EXISTS idx_artists_name ON artists(name);

-- Enable Row Level Security (RLS)
ALTER TABLE tracks ENABLE ROW LEVEL SECURITY;
ALTER TABLE artists ENABLE ROW LEVEL SECURITY;
ALTER TABLE albums ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access
CREATE POLICY "Allow public read access to tracks" ON tracks
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access to artists" ON artists
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access to albums" ON albums
    FOR SELECT USING (true);

-- Create policies for insert (you may want to add authentication later)
CREATE POLICY "Allow insert to tracks" ON tracks
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow delete to tracks" ON tracks
    FOR DELETE USING (true);

-- Insert sample data
INSERT INTO artists (name, bio) VALUES
    ('DJ Maphorisa', 'South African DJ, record producer, and singer'),
    ('Kabza De Small', 'South African DJ and record producer'),
    ('Master KG', 'South African musician and record producer'),
    ('DJ Stokie', 'South African DJ and record producer'),
    ('Mellow & Sleazy', 'South African Amapiano production duo');

INSERT INTO tracks (title, artist, album, genre, file_url, cover_url, plays) VALUES
    ('Siyathandana', 'DJ Maphorisa, Kabza De Small', 'Piano Hub', 'Amapiano', '/uploads/tracks/sample1.mp3', '/uploads/covers/cover1.jpg', 1523),
    ('Imithandazo', 'Kabza De Small, DJ Maphorisa', 'Scorpion Kings', 'Amapiano', '/uploads/tracks/sample2.mp3', '/uploads/covers/cover2.jpg', 2341),
    ('Jerusalema', 'Master KG', 'Jerusalema', 'Afro House', '/uploads/tracks/sample3.mp3', '/uploads/covers/cover3.jpg', 5672),
    ('Emcimbini', 'Kabza De Small, DJ Stokie', 'The Lele Lele Album', 'Amapiano', '/uploads/tracks/sample4.mp3', '/uploads/covers/cover4.jpg', 3421),
    ('Adiwele', 'Kabza De Small, DJ Maphorisa', 'Scorpion Kings Live', 'Amapiano', '/uploads/tracks/sample5.mp3', '/uploads/covers/cover5.jpg', 2876),
    ('Umshove', 'Mellow & Sleazy', 'Private School Amapiano', 'Amapiano', '/uploads/tracks/sample6.mp3', '/uploads/covers/cover6.jpg', 1987),
    ('Bambelela', 'DJ Stokie, Kabza De Small', 'Isimo', 'Amapiano', '/uploads/tracks/sample7.mp3', '/uploads/covers/cover7.jpg', 2134),
    ('Izolo', 'DJ Maphorisa, Kabza De Small', 'Piano Republic', 'Amapiano', '/uploads/tracks/sample8.mp3', '/uploads/covers/cover8.jpg', 3245),
    ('Ngiyazifela Ngawe', 'Kabza De Small', 'Ama Piano Selektah', 'Amapiano', '/uploads/tracks/sample9.mp3', '/uploads/covers/cover9.jpg', 4532),
    ('Dali Nguwe', 'Kabza De Small, DJ Maphorisa', 'Scorpion Kings', 'Amapiano', '/uploads/tracks/sample10.mp3', '/uploads/covers/cover10.jpg', 2987);

-- Create storage buckets for Supabase Storage (if using)
-- Note: Run these in Supabase Dashboard > Storage
-- CREATE BUCKET 'tracks' WITH (public = true);
-- CREATE BUCKET 'covers' WITH (public = true);
