# DGT-SOUNDS - Firebase Firestore Schema

This document describes the Firestore database structure for the DGT-SOUNDS music streaming platform.

## Collections Overview

### 1. `tracks`
Stores all music track metadata. Files are stored in Cloudflare R2.

**Document Structure:**
```javascript
{
  id: string,              // Auto-generated UUID
  title: string,           // Track title (required)
  artist: string,          // Artist name (required)
  album: string | null,    // Album name (optional)
  genre: string | null,    // Genre category (optional)
  duration: number,        // Duration in seconds (default: 0)
  file_url: string,        // Cloudflare R2 URL to audio file (required)
  cover_url: string | null,// Cloudflare R2 URL to cover art (optional)
  plays: number,           // Play count (default: 0)
  created_at: string       // ISO 8601 timestamp
}
```

**Indexes:**
- `created_at DESC` - For latest tracks query
- `plays DESC` - For featured/trending tracks
- `genre` - For genre filtering
- `artist` - For artist filtering

**Example Document:**
```javascript
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Siyathandana",
  "artist": "DJ Maphorisa, Kabza De Small",
  "album": "Piano Hub",
  "genre": "Amapiano",
  "duration": 245,
  "file_url": "https://pub-your-public-id.r2.dev/tracks/550e8400-e29b-41d4-a716-446655440000.mp3",
  "cover_url": "https://pub-your-public-id.r2.dev/covers/550e8400-e29b-41d4-a716-446655440000.jpg",
  "plays": 1523,
  "created_at": "2026-03-24T10:30:00Z"
}
```

---

### 2. `artists`
Stores artist information.

**Document Structure:**
```javascript
{
  id: string,              // Auto-generated UUID
  name: string,            // Artist name (required)
  bio: string | null,      // Artist biography (optional)
  image_url: string | null // Cloudflare R2 URL to artist image (optional)
}
```

**Indexes:**
- `name` - For artist search and sorting

**Example Document:**
```javascript
{
  "id": "artist-001",
  "name": "DJ Maphorisa",
  "bio": "South African DJ, record producer, and singer",
  "image_url": "https://pub-your-public-id.r2.dev/covers/artist_artist-001.jpg"
}
```

---

### 3. `albums`
Stores album information with references to artists.

**Document Structure:**
```javascript
{
  id: string,              // Auto-generated UUID
  title: string,           // Album title (required)
  artist_id: string,       // Reference to artists collection (required)
  artist_name: string | null, // Denormalized artist name for easier queries
  release_year: number | null, // Release year (optional)
  cover_url: string | null // Cloudflare R2 URL to album cover (optional)
}
```

**Indexes:**
- `artist_id` - For querying albums by artist

**Example Document:**
```javascript
{
  "id": "album-001",
  "title": "Scorpion Kings",
  "artist_id": "artist-001",
  "artist_name": "DJ Maphorisa",
  "release_year": 2019,
  "cover_url": "https://pub-your-public-id.r2.dev/covers/album_album-001.jpg"
}
```

---

## Cloudflare R2 Bucket Structure

### Bucket Organization
```
dgt-sounds/
├── tracks/
│   ├── {uuid}.mp3
│   ├── {uuid}.wav
│   └── {uuid}.flac
├── covers/
│   ├── {uuid}.jpg
│   ├── {uuid}.png
│   ├── album_{uuid}.jpg
│   └── artist_{uuid}.jpg
```

### File Naming Conventions
- **Tracks**: `{uuid}.{extension}`
- **Track Covers**: `{uuid}.{extension}`
- **Album Covers**: `album_{uuid}.{extension}`
- **Artist Images**: `artist_{uuid}.{extension}`

### CORS Configuration for R2
Make sure to configure CORS on your R2 bucket to allow public read access:

```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3600
    }
  ]
}
```

---

## Firestore Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Tracks - Public read, authenticated write
    match /tracks/{trackId} {
      allow read: if true;
      allow create, update, delete: if request.auth != null;
    }
    
    // Artists - Public read, authenticated write
    match /artists/{artistId} {
      allow read: if true;
      allow create, update, delete: if request.auth != null;
    }
    
    // Albums - Public read, authenticated write
    match /albums/{albumId} {
      allow read: if true;
      allow create, update, delete: if request.auth != null;
    }
  }
}
```

---

## Setup Instructions

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project named "DGT-SOUNDS"
3. Enable Firestore Database
4. Start in **production mode** or **test mode** (you can update rules later)

### 2. Download Service Account Credentials
1. In Firebase Console, go to **Project Settings** (gear icon)
2. Go to **Service accounts** tab
3. Click **Generate new private key**
4. Save the JSON file as `firebase_credentials.json` in the `backend/` folder

### 3. Create Firestore Indexes
In Firebase Console > Firestore > Indexes, create the following composite indexes:

| Collection | Fields | Query Scope |
|------------|--------|-------------|
| tracks | created_at (DESC) | Collection |
| tracks | plays (DESC) | Collection |
| tracks | genre (ASC), created_at (DESC) | Collection |
| tracks | artist (ASC), created_at (DESC) | Collection |

### 4. Set Up Cloudflare R2
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **R2**
3. Create a bucket named `dgt-sounds`
4. Create an **API Token** with read/write permissions
5. Note your **Account ID** from the R2 overview page
6. Configure CORS as shown above

### 5. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

---

## Migration from Supabase

If you're migrating from Supabase:

1. **Export data from Supabase** using SQL:
```sql
-- Export tracks
COPY tracks TO STDOUT WITH CSV HEADER;

-- Export artists
COPY artists TO STDOUT WITH CSV HEADER;

-- Export albums
COPY albums TO STDOUT WITH CSV HEADER;
```

2. **Import to Firestore** using a migration script or Firebase Admin SDK

3. **Migrate files** from Supabase Storage to Cloudflare R2 using a script

4. **Update URLs** in Firestore documents to point to new R2 URLs

---

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tracks` | Get all tracks |
| GET | `/api/tracks/{id}` | Get single track |
| POST | `/api/tracks` | Upload new track |
| DELETE | `/api/tracks/{id}` | Delete track |
| GET | `/api/artists` | Get all artists |
| GET | `/api/albums` | Get all albums |
| GET | `/api/genres` | Get all genres |
| GET | `/api/search?q=query` | Search tracks |
| GET | `/api/featured` | Get featured tracks |
| GET | `/api/latest` | Get latest tracks |

---

**Last Updated:** March 24, 2026
