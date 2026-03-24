"""
DGT-SOUNDS Backend API
FastAPI backend with Firebase Firestore (database) and Supabase Storage (files)
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

from firebase_client import get_db
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
        db = get_db()
        print("✅ Firebase Firestore connected")
    except Exception as e:
        print(f"❌ Firebase Firestore error: {e}")
    
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
def get_firestore():
    """Get Firestore client"""
    return get_db()

def track_from_doc(doc) -> dict:
    """Convert Firestore document to track dict"""
    data = doc.to_dict()
    return {
        "id": doc.id,
        **data
    }

def artist_from_doc(doc) -> dict:
    """Convert Firestore document to artist dict"""
    data = doc.to_dict()
    return {
        "id": doc.id,
        **data
    }

def album_from_doc(doc) -> dict:
    """Convert Firestore document to album dict"""
    data = doc.to_dict()
    return {
        "id": doc.id,
        **data
    }

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
        # Test Firebase connection
        db = get_firestore()
        db.collection("_health_check").document("test").get()
        firebase_status = "connected"
    except Exception as e:
        firebase_status = f"error: {str(e)}"
    
    try:
        # Test Supabase connection
        from supabase_storage_client import get_supabase
        get_supabase()
        supabase_status = "connected"
    except Exception as e:
        supabase_status = f"error: {str(e)}"
    
    return {
        "status": "ok",
        "firebase": firebase_status,
        "supabase": supabase_status
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
        db = get_firestore()
        tracks_ref = db.collection("tracks")

        query = tracks_ref.order_by("created_at", direction="DESCENDING")

        if genre:
            query = query.where("genre", "==", genre)

        if artist:
            query = query.where("artist", "==", artist)

        # Firestore doesn't support offset directly, so we fetch and slice
        docs = query.limit(limit + offset).stream()
        all_tracks = [track_from_doc(doc) for doc in docs]
        tracks = all_tracks[offset:] if offset > 0 else all_tracks

        return tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tracks/{track_id}", response_model=Track)
async def get_track(track_id: str):
    """Get a single track by ID"""
    try:
        db = get_firestore()
        doc_ref = db.collection("tracks").document(track_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Track not found")
        
        track = track_from_doc(doc)
        
        # Increment play count
        doc_ref.update({"plays": track.get("plays", 0) + 1})
        track["plays"] = track.get("plays", 0) + 1
        
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
        db = get_firestore()

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
                raise HTTPException(status_code=500, detail=f"Failed to upload cover image: {str(upload_error)}")

        # Insert into Firestore
        track_data = {
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

        doc_ref = db.collection("tracks").document(track_id)
        doc_ref.set(track_data)

        return {
            "id": track_id,
            **track_data
        }

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
        db = get_firestore()
        
        # Get track to delete files from Supabase Storage
        doc_ref = db.collection("tracks").document(track_id)
        doc = doc_ref.get()
        
        if doc.exists:
            track = doc.to_dict()
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
        
        # Delete from Firestore
        doc_ref.delete()
        
        return {"message": "Track deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artists", response_model=List[Artist])
async def get_artists(limit: int = Query(20, ge=1, le=100)):
    """Get all artists"""
    try:
        db = get_firestore()
        docs = db.collection("artists").limit(limit).stream()
        return [artist_from_doc(doc) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums", response_model=List[Album])
async def get_albums(limit: int = Query(20, ge=1, le=100)):
    """Get all albums"""
    try:
        db = get_firestore()
        docs = db.collection("albums").limit(limit).stream()
        
        albums = []
        for doc in docs:
            album_data = album_from_doc(doc)
            # Fetch artist name
            if album_data.get("artist_id"):
                artist_doc = db.collection("artists").document(album_data["artist_id"]).get()
                if artist_doc.exists:
                    album_data["artist_name"] = artist_doc.to_dict().get("name")
            albums.append(album_data)
        
        return albums
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/genres")
async def get_genres():
    """Get all unique genres"""
    try:
        db = get_firestore()
        docs = db.collection("tracks").stream()
        genres = list(set([doc.to_dict().get("genre") for doc in docs if doc.to_dict().get("genre")]))
        return {"genres": genres}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search(q: str = Query(..., min_length=1)):
    """Search tracks by title, artist, or album"""
    try:
        db = get_firestore()
        docs = db.collection("tracks").stream()
        
        query_lower = q.lower()
        results = []
        
        for doc in docs:
            track = doc.to_dict()
            if (query_lower in track.get("title", "").lower() or
                query_lower in track.get("artist", "").lower() or
                query_lower in track.get("album", "").lower()):
                results.append(track_from_doc(doc))
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/featured")
async def get_featured_tracks(limit: int = Query(10, ge=1, le=50)):
    """Get featured/trending tracks"""
    try:
        db = get_firestore()
        docs = db.collection("tracks").order_by("plays", direction="DESCENDING").limit(limit).stream()
        return [track_from_doc(doc) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/latest")
async def get_latest_tracks(limit: int = Query(10, ge=1, le=50)):
    """Get latest tracks"""
    try:
        db = get_firestore()
        docs = db.collection("tracks").order_by("created_at", direction="DESCENDING").limit(limit).stream()
        return [track_from_doc(doc) for doc in docs]
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
        db = get_firestore()
        update_data = {}
        if title: update_data["title"] = title
        if artist: update_data["artist"] = artist
        if album: update_data["album"] = album
        if genre: update_data["genre"] = genre

        doc_ref = db.collection("tracks").document(track_id)
        doc_ref.update(update_data)
        
        updated_doc = doc_ref.get()
        return track_from_doc(updated_doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/tracks/{track_id}")
async def admin_delete_track(track_id: str, authorization: str = Header(None)):
    """Delete a track (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

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
        db = get_firestore()
        album_id = str(uuid.uuid4())
        
        cover_url = None
        if cover:
            cover_extension = cover.filename.split(".")[-1] if cover.filename else "jpg"
            cover_path = f"covers/album_{album_id}.{cover_extension}"
            
            cover_content = await cover.read()
            cover_content_type = cover.content_type or "image/jpeg"
            cover_url = upload_file(cover_content, "covers", cover_path, cover_content_type)
        
        album_data = {
            "title": title,
            "artist_id": artist_id,
            "release_year": release_year,
            "cover_url": cover_url
        }
        
        db.collection("albums").document(album_id).set(album_data)
        
        return {
            "id": album_id,
            **album_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/albums/{album_id}")
async def delete_album(album_id: str, authorization: str = Header(None)):
    """Delete an album (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        db = get_firestore()
        
        # Get album to delete cover from Supabase Storage
        doc_ref = db.collection("albums").document(album_id)
        doc = doc_ref.get()
        
        if doc.exists:
            album = doc.to_dict()
            if album.get("cover_url"):
                cover_path = album["cover_url"].split("/covers/")[-1]
                try:
                    delete_file("covers", cover_path)
                except:
                    pass
        
        doc_ref.delete()
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
        db = get_firestore()
        artist_id = str(uuid.uuid4())
        
        image_url = None
        if image:
            image_extension = image.filename.split(".")[-1] if image.filename else "jpg"
            image_path = f"covers/artist_{artist_id}.{image_extension}"
            
            image_content = await image.read()
            image_content_type = image.content_type or "image/jpeg"
            image_url = upload_file(image_content, "covers", image_path, image_content_type)
        
        artist_data = {
            "name": name,
            "bio": bio,
            "image_url": image_url
        }
        
        db.collection("artists").document(artist_id).set(artist_data)
        
        return {
            "id": artist_id,
            **artist_data
        }
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
        db = get_firestore()
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

        doc_ref = db.collection("artists").document(artist_id)
        doc_ref.update(update_data)
        
        updated_doc = doc_ref.get()
        return artist_from_doc(updated_doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/artists/{artist_id}")
async def delete_artist(artist_id: str, authorization: str = Header(None)):
    """Delete an artist (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        db = get_firestore()
        
        # Get artist to delete image from Supabase Storage
        doc_ref = db.collection("artists").document(artist_id)
        doc = doc_ref.get()
        
        if doc.exists:
            artist = doc.to_dict()
            if artist.get("image_url"):
                image_path = artist["image_url"].split("/covers/")[-1]
                try:
                    delete_file("covers", image_path)
                except:
                    pass
        
        doc_ref.delete()
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
