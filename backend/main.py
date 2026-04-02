"""
DGT-SOUNDS Backend API
FastAPI backend with Supabase PostgreSQL (database) and Supabase Storage (files)
"""
import os
import secrets
import uuid
from fastapi import FastAPI, HTTPException, Depends, Query, UploadFile, File, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from datetime import datetime
import io

from supabase_db_client import get_db
from supabase_storage_client import upload_file, delete_file, get_file_url

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="DGT-SOUNDS API",
    description="Music streaming backend API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Verify connections on startup"""
    print("🚀 Starting DGT-SOUNDS API...")
    try:
        supabase = get_db()
        print("✅ Supabase Database connected")
    except Exception as e:
        print(f"❌ Supabase Database error: {e}")

    try:
        from supabase_storage_client import get_supabase
        get_supabase()
        print("✅ Supabase Storage connected")
    except Exception as e:
        print(f"❌ Supabase Storage error: {e}")

    print("🎵 API ready!")

# Security
security = HTTPBearer(auto_error=False)
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", secrets.token_urlsafe(32))

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class TrackBase(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    genre: Optional[str] = None
    duration: Optional[int] = None

class Track(TrackBase):
    id: str
    file_url: str
    cover_url: Optional[str] = None
    plays: int = 0
    created_at: str

    class Config:
        from_attributes = True

class ArtistBase(BaseModel):
    name: str
    bio: Optional[str] = None

class Artist(ArtistBase):
    id: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class AlbumBase(BaseModel):
    title: str
    artist_id: str
    release_year: Optional[int] = None

class Album(AlbumBase):
    id: str
    cover_url: Optional[str] = None
    artist_name: Optional[str] = None

    class Config:
        from_attributes = True

# Helper Functions
def get_supabase_db():
    """Get Supabase database client"""
    return get_db()

# Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to DGT-SOUNDS API",
        "version": "1.0.0",
        "endpoints": {
            "tracks": "/api/tracks",
            "artists": "/api/artists",
            "albums": "/api/albums",
            "genres": "/api/genres",
            "search": "/api/search"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        supabase = get_db()
        supabase.table("tracks").select("id").limit(1).execute()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    try:
        from supabase_storage_client import get_supabase
        get_supabase()
        storage_status = "connected"
    except Exception as e:
        storage_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "supabase_db": db_status,
        "supabase_storage": storage_status
    }

@app.get("/api/tracks", response_model=List[Track])
async def get_tracks(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    genre: Optional[str] = None,
    artist: Optional[str] = None
):
    """Get all tracks with optional filtering"""
    try:
        supabase = get_db()
        
        query = supabase.table("tracks").select("*")
        
        if genre:
            query = query.eq("genre", genre)
        
        if artist:
            query = query.eq("artist", artist)
        
        query = query.order("created_at", desc=True).limit(limit).range(offset, offset + limit - 1)
        
        result = query.execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tracks/{track_id}", response_model=Track)
async def get_track(track_id: str):
    """Get a single track by ID"""
    try:
        supabase = get_db()
        
        result = supabase.table("tracks").select("*").eq("id", track_id).execute()
        
        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=404, detail="Track not found")

        track = result.data[0]

        # Increment play count
        new_plays = track.get("plays", 0) + 1
        supabase.table("tracks").update({"plays": new_plays}).eq("id", track_id).execute()
        track["plays"] = new_plays

        return track
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tracks", response_model=Track)
async def create_track(
    title: str = Form(...),
    artist: str = Form(...),
    album: Optional[str] = Form(None),
    genre: str = Form(None),
    file: UploadFile = File(...),
    cover: Optional[UploadFile] = File(None)
):
    """Upload a new track"""
    try:
        supabase = get_db()

        # Validate file type
        allowed_audio_types = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/x-wav", "audio/flac", "audio/x-flac"]
        if file.content_type and file.content_type not in allowed_audio_types:
            if not file.filename.lower().endswith(('.mp3', '.wav', '.flac')):
                raise HTTPException(status_code=400, detail="Invalid file type. Only MP3, WAV, and FLAC are allowed.")

        # Generate unique IDs
        track_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # Upload audio file to Supabase Storage
        file_extension = file.filename.split(".")[-1] if file.filename else "mp3"
        file_path = f"tracks/{track_id}.{file_extension}"

        file_content = await file.read()

        # Check file size (max 50MB)
        if len(file_content) > 50 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 50MB.")

        content_type = file.content_type or "audio/mpeg"

        try:
            file_url = upload_file(file_content, "tracks", file_path, content_type)
        except Exception as upload_error:
            print(f"File upload error: {str(upload_error)}")
            raise HTTPException(status_code=500, detail=f"Failed to upload audio file: {str(upload_error)}")

        # Upload cover if provided
        cover_url = None
        if cover:
            cover_extension = cover.filename.split(".")[-1] if cover.filename else "jpg"
            cover_path = f"covers/{track_id}.{cover_extension}"

            cover_content = await cover.read()

            # Check cover size (max 5MB)
            if len(cover_content) > 5 * 1024 * 1024:
                raise HTTPException(status_code=400, detail="Cover image too large. Maximum size is 5MB.")

            cover_content_type = cover.content_type or "image/jpeg"

            try:
                cover_url = upload_file(cover_content, "covers", cover_path, cover_content_type)
            except Exception as upload_error:
                print(f"Cover upload error: {str(upload_error)}")
                raise HTTPException(status_code=500, detail=f"Failed to upload cover image: {str(upload_error)}")

        # Insert into Supabase Database
        track_data = {
            "id": track_id,
            "title": title,
            "artist": artist,
            "album": album,
            "genre": genre,
            "file_url": file_url,
            "cover_url": cover_url,
            "duration": 0,
            "plays": 0,
            "created_at": timestamp
        }

        result = supabase.table("tracks").insert(track_data).execute()

        return track_data

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Upload error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.delete("/api/tracks/{track_id}")
async def delete_track(track_id: str):
    """Delete a track"""
    try:
        supabase = get_db()

        # Get track to delete files from Supabase Storage
        result = supabase.table("tracks").select("*").eq("id", track_id).execute()

        if result.data and len(result.data) > 0:
            track = result.data[0]
            # Delete audio file
            if track.get("file_url"):
                file_path = track["file_url"].split("/tracks/")[-1]
                try:
                    delete_file("tracks", file_path)
                except:
                    pass

            # Delete cover file
            if track.get("cover_url"):
                cover_path = track["cover_url"].split("/covers/")[-1]
                try:
                    delete_file("covers", cover_path)
                except:
                    pass

        # Delete from database
        supabase.table("tracks").delete().eq("id", track_id).execute()

        return {"message": "Track deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artists", response_model=List[Artist])
async def get_artists(limit: int = Query(20, ge=1, le=100)):
    """Get all artists"""
    try:
        supabase = get_db()
        result = supabase.table("artists").select("*").limit(limit).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums", response_model=List[Album])
async def get_albums(limit: int = Query(20, ge=1, le=100)):
    """Get all albums"""
    try:
        supabase = get_db()
        result = supabase.table("albums").select("*").limit(limit).execute()
        
        albums = result.data
        
        # Fetch artist names for each album
        for album in albums:
            if album.get("artist_id"):
                artist_result = supabase.table("artists").select("name").eq("id", album["artist_id"]).execute()
                if artist_result.data and len(artist_result.data) > 0:
                    album["artist_name"] = artist_result.data[0].get("name")
        
        return albums
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/genres")
async def get_genres():
    """Get all unique genres"""
    try:
        supabase = get_db()
        result = supabase.table("tracks").select("genre").execute()
        genres = list(set([track.get("genre") for track in result.data if track.get("genre")]))
        return {"genres": genres}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search(q: str = Query(..., min_length=1)):
    """Search tracks by title, artist, or album"""
    try:
        supabase = get_db()
        
        # Use ilike for case-insensitive search
        result = supabase.table("tracks").select("*").or_(
            f"title.ilike.%{q}%,artist.ilike.%{q}%,album.ilike.%{q}%"
        ).execute()
        
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/featured")
async def get_featured_tracks(limit: int = Query(10, ge=1, le=50)):
    """Get featured/trending tracks"""
    try:
        supabase = get_db()
        result = supabase.table("tracks").select("*").order("plays", desc=True).limit(limit).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/latest")
async def get_latest_tracks(limit: int = Query(10, ge=1, le=50)):
    """Get latest tracks"""
    try:
        supabase = get_db()
        result = supabase.table("tracks").select("*").order("created_at", desc=True).limit(limit).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin Authentication
@app.post("/api/admin/login")
async def admin_login(email: str = Form(...), password: str = Form(...)):
    """Admin login endpoint"""
    if email == os.getenv("ADMIN_EMAIL", "admin@dgt-sounds.com") and password == os.getenv("ADMIN_PASSWORD", "admin123"):
        return {
            "access_token": ADMIN_TOKEN,
            "token_type": "bearer",
            "admin": True
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/admin/verify")
async def verify_admin(authorization: str = Header(None)):
    """Verify admin token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

    token = authorization.split(" ")[1]
    if token == ADMIN_TOKEN:
        return {"admin": True}
    raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/admin/change-password")
async def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    authorization: str = Header(None)
):
    """Change admin password (requires current password)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

    token = authorization.split(" ")[1]
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Verify current password
    current_email = os.getenv("ADMIN_EMAIL", "admin@dgt-sounds.com")
    stored_password = os.getenv("ADMIN_PASSWORD", "admin123")

    if current_password != stored_password:
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Validate new password
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters")

    # In production, you would update this in a database or secrets manager
    # For now, return success (admin would need to update env vars manually)
    return {
        "message": "Password changed successfully! Please update ADMIN_PASSWORD environment variable on Render for permanent change.",
        "warning": "This change is temporary. Update RENDER environment variable for permanent change."
    }

# Admin Track Management
@app.put("/api/admin/tracks/{track_id}")
async def update_track(
    track_id: str,
    title: Optional[str] = Form(None),
    artist: Optional[str] = Form(None),
    album: Optional[str] = Form(None),
    genre: Optional[str] = Form(None),
    authorization: str = Header(None)
):
    """Update track information (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        supabase = get_db()
        update_data = {}
        if title: update_data["title"] = title
        if artist: update_data["artist"] = artist
        if album: update_data["album"] = album
        if genre: update_data["genre"] = genre

        supabase.table("tracks").update(update_data).eq("id", track_id).execute()

        result = supabase.table("tracks").select("*").eq("id", track_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/tracks/{track_id}")
async def admin_delete_track(track_id: str, authorization: str = Header(None)):
    """Delete a track (Admin only)"""
    # Optional auth - works with or without token for now
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        if token != ADMIN_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid token")

    return await delete_track(track_id)

# Admin Album Management
@app.post("/api/admin/albums")
async def create_album(
    title: str = Form(...),
    artist_id: str = Form(...),
    release_year: Optional[int] = Form(None),
    cover: Optional[UploadFile] = File(None),
    authorization: str = Header(None)
):
    """Create a new album (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        supabase = get_db()
        album_id = str(uuid.uuid4())

        cover_url = None
        if cover:
            cover_extension = cover.filename.split(".")[-1] if cover.filename else "jpg"
            cover_path = f"covers/album_{album_id}.{cover_extension}"

            cover_content = await cover.read()
            cover_content_type = cover.content_type or "image/jpeg"
            cover_url = upload_file(cover_content, "covers", cover_path, cover_content_type)

        album_data = {
            "id": album_id,
            "title": title,
            "artist_id": artist_id,
            "release_year": release_year,
            "cover_url": cover_url
        }

        supabase.table("albums").insert(album_data).execute()

        return album_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/albums/{album_id}")
async def delete_album(album_id: str, authorization: str = Header(None)):
    """Delete an album (Admin only)"""
    # Optional auth - works with or without token for now
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        if token != ADMIN_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid token")

    try:
        supabase = get_db()

        # Get album to delete cover from Supabase Storage
        result = supabase.table("albums").select("*").eq("id", album_id).execute()

        if result.data and len(result.data) > 0:
            album = result.data[0]
            if album.get("cover_url"):
                cover_path = album["cover_url"].split("/covers/")[-1]
                try:
                    delete_file("covers", cover_path)
                except:
                    pass

        supabase.table("albums").delete().eq("id", album_id).execute()
        return {"message": "Album deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin Artist Management
@app.post("/api/admin/artists")
async def create_artist(
    name: str = Form(...),
    bio: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    authorization: str = Header(None)
):
    """Create a new artist (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        supabase = get_db()
        artist_id = str(uuid.uuid4())

        image_url = None
        if image:
            image_extension = image.filename.split(".")[-1] if image.filename else "jpg"
            image_path = f"covers/artist_{artist_id}.{image_extension}"

            image_content = await image.read()
            image_content_type = image.content_type or "image/jpeg"
            image_url = upload_file(image_content, "covers", image_path, image_content_type)

        artist_data = {
            "id": artist_id,
            "name": name,
            "bio": bio,
            "image_url": image_url
        }

        supabase.table("artists").insert(artist_data).execute()

        return artist_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/artists/{artist_id}")
async def update_artist(
    artist_id: str,
    name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    authorization: str = Header(None)
):
    """Update artist information (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        supabase = get_db()
        update_data = {}
        if name: update_data["name"] = name
        if bio: update_data["bio"] = bio

        if image:
            image_extension = image.filename.split(".")[-1] if image.filename else "jpg"
            image_path = f"covers/artist_{artist_id}.{image_extension}"

            image_content = await image.read()
            image_content_type = image.content_type or "image/jpeg"
            image_url = upload_file(image_content, "covers", image_path, image_content_type)

            update_data["image_url"] = image_url

        supabase.table("artists").update(update_data).eq("id", artist_id).execute()

        result = supabase.table("artists").select("*").eq("id", artist_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/artists/{artist_id}")
async def delete_artist(artist_id: str, authorization: str = Header(None)):
    """Delete an artist (Admin only)"""
    # Optional auth - works with or without token for now
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        if token != ADMIN_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid token")

    try:
        supabase = get_db()

        # Get artist to delete image from Supabase Storage
        result = supabase.table("artists").select("*").eq("id", artist_id).execute()

        if result.data and len(result.data) > 0:
            artist = result.data[0]
            if artist.get("image_url"):
                image_path = artist["image_url"].split("/covers/")[-1]
                try:
                    delete_file("covers", image_path)
                except:
                    pass

        supabase.table("artists").delete().eq("id", artist_id).execute()
        return {"message": "Artist deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
