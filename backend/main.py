"""
DGT-SOUNDS Backend API
FastAPI backend with Supabase integration for music streaming
"""
import os
import secrets
from fastapi import FastAPI, HTTPException, Depends, Query, UploadFile, File, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
import aiofiles
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="DGT-SOUNDS API",
    description="Music streaming backend API",
    version="1.0.0"
)

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

# Supabase Client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Directories
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
(UPLOAD_DIR / "tracks").mkdir(exist_ok=True)
(UPLOAD_DIR / "covers").mkdir(exist_ok=True)

# Pydantic Models
class TrackBase(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    genre: Optional[str] = None
    duration: Optional[int] = None

class TrackCreate(TrackBase):
    pass

class Track(TrackBase):
    id: int
    file_url: str
    cover_url: Optional[str] = None
    plays: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

class ArtistBase(BaseModel):
    name: str
    bio: Optional[str] = None

class Artist(ArtistBase):
    id: int
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class AlbumBase(BaseModel):
    title: str
    artist_id: int
    release_year: Optional[int] = None

class Album(AlbumBase):
    id: int
    cover_url: Optional[str] = None
    
    class Config:
        from_attributes = True

# Helper Functions
def get_db():
    """Get Supabase client"""
    return supabase

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

@app.get("/api/tracks", response_model=List[Track])
async def get_tracks(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    genre: Optional[str] = None,
    artist: Optional[str] = None
):
    """Get all tracks with optional filtering"""
    try:
        query = supabase.table("tracks").select("*")
        
        if genre:
            query = query.eq("genre", genre)
        
        if artist:
            query = query.eq("artist", artist)
        
        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tracks/{track_id}", response_model=Track)
async def get_track(track_id: int):
    """Get a single track by ID"""
    try:
        response = supabase.table("tracks").select("*").eq("id", track_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Track not found")
        
        # Increment play count
        supabase.table("tracks").rpc("increment_plays", {"track_id": track_id}).execute()
        
        return response.data[0]
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
        # Save audio file
        file_extension = file.filename.split(".")[-1] if file.filename else "mp3"
        file_path = UPLOAD_DIR / "tracks" / f"{datetime.now().timestamp()}_{file.filename}"
        
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Save cover if provided
        cover_url = None
        if cover:
            cover_extension = cover.filename.split(".")[-1] if cover.filename else "jpg"
            cover_path = UPLOAD_DIR / "covers" / f"{datetime.now().timestamp()}_{cover.filename}"
            
            async with aiofiles.open(cover_path, "wb") as out_file:
                content = await cover.read()
                await out_file.write(content)
            
            cover_url = f"/uploads/covers/{cover_path.name}"
        
        # Insert into database
        track_data = {
            "title": title,
            "artist": artist,
            "album": album,
            "genre": genre,
            "file_url": f"/uploads/tracks/{file_path.name}",
            "cover_url": cover_url,
            "duration": 0
        }
        
        response = supabase.table("tracks").insert(track_data).execute()
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/tracks/{track_id}")
async def delete_track(track_id: int):
    """Delete a track"""
    try:
        response = supabase.table("tracks").delete().eq("id", track_id).execute()
        return {"message": "Track deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artists", response_model=List[Artist])
async def get_artists(limit: int = Query(20, ge=1, le=100)):
    """Get all artists"""
    try:
        response = supabase.table("artists").select("*").limit(limit).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/albums", response_model=List[Album])
async def get_albums(limit: int = Query(20, ge=1, le=100)):
    """Get all albums"""
    try:
        response = supabase.table("albums").select("*").limit(limit).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/genres")
async def get_genres():
    """Get all unique genres"""
    try:
        response = supabase.table("tracks").select("genre").execute()
        genres = list(set([track["genre"] for track in response.data if track.get("genre")]))
        return {"genres": genres}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search(q: str = Query(..., min_length=1)):
    """Search tracks by title, artist, or album"""
    try:
        response = supabase.table("tracks").select("*").or_(
            f"title.ilike.%{q}%,artist.ilike.%{q}%,album.ilike.%{q}%"
        ).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/featured")
async def get_featured_tracks(limit: int = Query(10, ge=1, le=50)):
    """Get featured/trending tracks"""
    try:
        response = supabase.table("tracks").select("*").order("plays", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/latest")
async def get_latest_tracks(limit: int = Query(10, ge=1, le=50)):
    """Get latest tracks"""
    try:
        response = supabase.table("tracks").select("*").order("created_at", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin Authentication
@app.post("/api/admin/login")
async def admin_login(email: str = Form(...), password: str = Form(...)):
    """Admin login endpoint"""
    # Simple auth - in production use proper authentication
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
    track_id: int,
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
        update_data = {}
        if title: update_data["title"] = title
        if artist: update_data["artist"] = artist
        if album: update_data["album"] = album
        if genre: update_data["genre"] = genre
        
        response = supabase.table("tracks").update(update_data).eq("id", track_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/tracks/{track_id}")
async def admin_delete_track(track_id: int, authorization: str = Header(None)):
    """Delete a track (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    
    try:
        response = supabase.table("tracks").delete().eq("id", track_id).execute()
        return {"message": "Track deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin Album Management
@app.post("/api/admin/albums")
async def create_album(
    title: str = Form(...),
    artist_id: int = Form(...),
    release_year: Optional[int] = Form(None),
    cover: Optional[UploadFile] = File(None),
    authorization: str = Header(None)
):
    """Create a new album (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    
    try:
        cover_url = None
        if cover:
            cover_extension = cover.filename.split(".")[-1] if cover.filename else "jpg"
            cover_path = UPLOAD_DIR / "covers" / f"album_{datetime.now().timestamp()}_{cover.filename}"
            
            async with aiofiles.open(cover_path, "wb") as out_file:
                content = await cover.read()
                await out_file.write(content)
            
            cover_url = f"/uploads/covers/{cover_path.name}"
        
        album_data = {
            "title": title,
            "artist_id": artist_id,
            "release_year": release_year,
            "cover_url": cover_url
        }
        
        response = supabase.table("albums").insert(album_data).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/albums/{album_id}")
async def delete_album(album_id: int, authorization: str = Header(None)):
    """Delete an album (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    
    try:
        response = supabase.table("albums").delete().eq("id", album_id).execute()
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
        image_url = None
        if image:
            image_extension = image.filename.split(".")[-1] if image.filename else "jpg"
            image_path = UPLOAD_DIR / "covers" / f"artist_{datetime.now().timestamp()}_{image.filename}"
            
            async with aiofiles.open(image_path, "wb") as out_file:
                content = await image.read()
                await out_file.write(content)
            
            image_url = f"/uploads/covers/{image_path.name}"
        
        artist_data = {
            "name": name,
            "bio": bio,
            "image_url": image_url
        }
        
        response = supabase.table("artists").insert(artist_data).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/artists/{artist_id}")
async def update_artist(
    artist_id: int,
    name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    authorization: str = Header(None)
):
    """Update artist information (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    
    try:
        update_data = {}
        if name: update_data["name"] = name
        if bio: update_data["bio"] = bio
        
        if image:
            image_extension = image.filename.split(".")[-1] if image.filename else "jpg"
            image_path = UPLOAD_DIR / "covers" / f"artist_{datetime.now().timestamp()}_{image.filename}"
            
            async with aiofiles.open(image_path, "wb") as out_file:
                content = await image.read()
                await out_file.write(content)
            
            update_data["image_url"] = f"/uploads/covers/{image_path.name}"
        
        response = supabase.table("artists").update(update_data).eq("id", artist_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/artists/{artist_id}")
async def delete_artist(artist_id: int, authorization: str = Header(None)):
    """Delete an artist (Admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    
    try:
        response = supabase.table("artists").delete().eq("id", artist_id).execute()
        return {"message": "Artist deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
