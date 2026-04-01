-- ============================================
-- DGT-SOUNDS - Complete Supabase Setup
-- Run this in Supabase SQL Editor
-- ============================================

-- 1. Create tracks table
CREATE TABLE IF NOT EXISTS tracks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT,
    genre TEXT,
    file_url TEXT NOT NULL,
    cover_url TEXT,
    duration INTEGER DEFAULT 0,
    plays INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create artists table
CREATE TABLE IF NOT EXISTS artists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    bio TEXT,
    image_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Create albums table
CREATE TABLE IF NOT EXISTS albums (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    artist_id UUID REFERENCES artists(id),
    release_year INTEGER,
    cover_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tracks_genre ON tracks(genre);
CREATE INDEX IF NOT EXISTS idx_tracks_artist ON tracks(artist);
CREATE INDEX IF NOT EXISTS idx_tracks_created_at ON tracks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tracks_plays ON tracks(plays DESC);
CREATE INDEX IF NOT EXISTS idx_artists_name ON artists(name);
CREATE INDEX IF NOT EXISTS idx_albums_artist_id ON albums(artist_id);

-- ============================================
-- Storage Buckets (run if buckets don't exist)
-- ============================================

-- Create tracks bucket
INSERT INTO storage.buckets (id, name, public) 
VALUES ('tracks', 'tracks', true)
ON CONFLICT (id) DO NOTHING;

-- Create covers bucket
INSERT INTO storage.buckets (id, name, public) 
VALUES ('covers', 'covers', true)
ON CONFLICT (id) DO NOTHING;

-- ============================================
-- Storage Policies
-- ============================================

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Public Read - Tracks" ON storage.objects;
DROP POLICY IF EXISTS "Upload - Tracks" ON storage.objects;
DROP POLICY IF EXISTS "Delete - Tracks" ON storage.objects;
DROP POLICY IF EXISTS "Public Read - Covers" ON storage.objects;
DROP POLICY IF EXISTS "Upload - Covers" ON storage.objects;
DROP POLICY IF EXISTS "Delete - Covers" ON storage.objects;

-- Tracks bucket policies
CREATE POLICY "Public Read - Tracks" ON storage.objects
FOR SELECT USING (bucket_id = 'tracks');

CREATE POLICY "Upload - Tracks" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'tracks');

CREATE POLICY "Delete - Tracks" ON storage.objects
FOR DELETE USING (bucket_id = 'tracks');

-- Covers bucket policies
CREATE POLICY "Public Read - Covers" ON storage.objects
FOR SELECT USING (bucket_id = 'covers');

CREATE POLICY "Upload - Covers" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'covers');

CREATE POLICY "Delete - Covers" ON storage.objects
FOR DELETE USING (bucket_id = 'covers');

-- ============================================
-- Sample Data (Optional)
-- ============================================

-- Sample Artist
INSERT INTO artists (id, name, bio) VALUES 
('00000000-0000-0000-0000-000000000001', 'Sample Artist', 'This is a sample artist')
ON CONFLICT (id) DO NOTHING;

-- Sample Album
INSERT INTO albums (id, title, artist_id, release_year) VALUES 
('00000000-0000-0000-0000-000000000001', 'Sample Album', '00000000-0000-0000-0000-000000000001', 2024)
ON CONFLICT (id) DO NOTHING;
