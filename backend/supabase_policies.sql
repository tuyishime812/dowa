-- DGT-SOUNDS Supabase Storage Policies
-- Run these SQL commands in Supabase SQL Editor
-- 
-- IMPORTANT: Run each section separately if you get errors

-- ============================================
-- STEP 1: Create Buckets (if not already created)
-- ============================================
-- Note: If buckets already exist, skip this section

-- Create tracks bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('tracks', 'tracks', true)
ON CONFLICT (id) DO NOTHING;

-- Create covers bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('covers', 'covers', true)
ON CONFLICT (id) DO NOTHING;

-- ============================================
-- STEP 2: Drop Existing Policies (if any)
-- ============================================
-- This prevents "policy already exists" errors

DROP POLICY IF EXISTS "Public Read Access - Tracks" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated Upload - Tracks" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated Update - Tracks" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated Delete - Tracks" ON storage.objects;

DROP POLICY IF EXISTS "Public Read Access - Covers" ON storage.objects;
DROP POLICY IF EXISTS "Public Upload - Covers" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated Upload - Covers" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated Update - Covers" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated Delete - Covers" ON storage.objects;

-- ============================================
-- STEP 3: Create Policies for TRACKS Bucket
-- ============================================

-- Policy 1: Allow public read access to tracks bucket
CREATE POLICY "Public Read Access - Tracks"
ON storage.objects FOR SELECT
USING (bucket_id = 'tracks');

-- Policy 2: Allow anyone to upload to tracks bucket
CREATE POLICY "Public Upload - Tracks"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'tracks');

-- Policy 3: Allow anyone to update files in tracks bucket
CREATE POLICY "Public Update - Tracks"
ON storage.objects FOR UPDATE
USING (bucket_id = 'tracks');

-- Policy 4: Allow anyone to delete files in tracks bucket
CREATE POLICY "Public Delete - Tracks"
ON storage.objects FOR DELETE
USING (bucket_id = 'tracks');

-- ============================================
-- STEP 4: Create Policies for COVERS Bucket
-- ============================================

-- Policy 1: Allow public read access to covers bucket
CREATE POLICY "Public Read Access - Covers"
ON storage.objects FOR SELECT
USING (bucket_id = 'covers');

-- Policy 2: Allow anyone to upload to covers bucket
CREATE POLICY "Public Upload - Covers"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'covers');

-- Policy 3: Allow anyone to update files in covers bucket
CREATE POLICY "Public Update - Covers"
ON storage.objects FOR UPDATE
USING (bucket_id = 'covers');

-- Policy 4: Allow anyone to delete files in covers bucket
CREATE POLICY "Public Delete - Covers"
ON storage.objects FOR DELETE
USING (bucket_id = 'covers');

-- ============================================
-- DONE! Verify policies are created
-- ============================================
-- You should see 8 policies total (4 for tracks, 4 for covers)
