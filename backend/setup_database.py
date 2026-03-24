"""
Database Setup Script
Initialize Firestore with sample data for DGT-SOUNDS
"""
import os
from firebase_client import get_db
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def create_sample_data():
    """Create sample artists, albums, and tracks"""
    db = get_db()
    
    print("🎵 Creating sample data for DGT-SOUNDS...")
    
    # Sample Artists
    artists_data = [
        {"name": "DJ Maphorisa", "bio": "South African DJ, record producer, and singer"},
        {"name": "Kabza De Small", "bio": "South African DJ and record producer, king of Amapiano"},
        {"name": "Master KG", "bio": "South African musician and record producer"},
        {"name": "DJ Stokie", "bio": "South African DJ and record producer"},
        {"name": "Mellow & Sleazy", "bio": "South African Amapiano production duo"},
    ]
    
    print("\n📀 Creating artists...")
    artist_ids = []
    for artist in artists_data:
        doc_ref = db.collection("artists").add(artist)
        artist_ids.append(doc_ref[1].id)
        print(f"  ✅ Added: {artist['name']}")
    
    # Sample Albums
    albums_data = [
        {"title": "Scorpion Kings", "artist_id": artist_ids[1], "release_year": 2019},
        {"title": "Piano Hub", "artist_id": artist_ids[0], "release_year": 2020},
        {"title": "Jerusalema", "artist_id": artist_ids[2], "release_year": 2019},
        {"title": "The Lele Lele Album", "artist_id": artist_ids[3], "release_year": 2021},
    ]
    
    print("\n💿 Creating albums...")
    album_ids = []
    for album in albums_data:
        doc_ref = db.collection("albums").add(album)
        album_ids.append(doc_ref[1].id)
        print(f"  ✅ Added: {album['title']}")
    
    # Sample Tracks (with placeholder URLs - update with real files)
    tracks_data = [
        {
            "title": "Siyathandana",
            "artist": "DJ Maphorisa, Kabza De Small",
            "album": "Piano Hub",
            "genre": "Amapiano",
            "duration": 245,
            "plays": 1523,
            "file_url": "https://via.placeholder.com/track1.mp3",
            "cover_url": "https://via.placeholder.com/cover1.jpg"
        },
        {
            "title": "Imithandazo",
            "artist": "Kabza De Small, DJ Maphorisa",
            "album": "Scorpion Kings",
            "genre": "Amapiano",
            "duration": 312,
            "plays": 2341,
            "file_url": "https://via.placeholder.com/track2.mp3",
            "cover_url": "https://via.placeholder.com/cover2.jpg"
        },
        {
            "title": "Jerusalema",
            "artist": "Master KG",
            "album": "Jerusalema",
            "genre": "Afro House",
            "duration": 218,
            "plays": 5672,
            "file_url": "https://via.placeholder.com/track3.mp3",
            "cover_url": "https://via.placeholder.com/cover3.jpg"
        },
        {
            "title": "Emcimbini",
            "artist": "Kabza De Small, DJ Stokie",
            "album": "The Lele Lele Album",
            "genre": "Amapiano",
            "duration": 367,
            "plays": 3421,
            "file_url": "https://via.placeholder.com/track4.mp3",
            "cover_url": "https://via.placeholder.com/cover4.jpg"
        },
        {
            "title": "Adiwele",
            "artist": "Kabza De Small, DJ Maphorisa",
            "album": "Scorpion Kings Live",
            "genre": "Amapiano",
            "duration": 289,
            "plays": 2876,
            "file_url": "https://via.placeholder.com/track5.mp3",
            "cover_url": "https://via.placeholder.com/cover5.jpg"
        },
    ]
    
    print("\n🎶 Creating tracks...")
    for track in tracks_data:
        track["created_at"] = datetime.now().isoformat()
        doc_ref = db.collection("tracks").add(track)
        print(f"  ✅ Added: {track['title']} - {track['artist']}")
    
    print("\n" + "="*50)
    print("✅ Sample data created successfully!")
    print("="*50)
    print(f"\n📊 Summary:")
    print(f"   Artists: {len(artists_data)}")
    print(f"   Albums: {len(albums_data)}")
    print(f"   Tracks: {len(tracks_data)}")
    print("\n🎵 You can now start the server and test the API!")
    print("   Run: python main.py")

if __name__ == "__main__":
    try:
        create_sample_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Firebase credentials file exists (firebase_credentials.json)")
        print("  2. You have internet connection")
        print("  3. Firebase Firestore is enabled in your project")
