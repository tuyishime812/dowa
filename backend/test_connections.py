"""
Test Connections Script
Verify Firebase and Supabase connections are working
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_firebase():
    """Test Firebase Firestore connection"""
    print("\n🔥 Testing Firebase Firestore...")
    try:
        from firebase_client import get_db
        db = get_db()
        
        # Try to read from a collection
        docs = db.collection("_test").limit(1).stream()
        _ = list(docs)  # Execute the query
        
        print("   ✅ Firebase Firestore: CONNECTED")
        return True
    except FileNotFoundError as e:
        print(f"   ❌ Firebase credentials file not found!")
        print(f"      Error: {e}")
        print("\n      Solution:")
        print("      1. Download firebase_credentials.json from Firebase Console")
        print("      2. Place it in the backend folder")
        return False
    except Exception as e:
        print(f"   ❌ Firebase Firestore: ERROR")
        print(f"      Error: {e}")
        return False

def test_supabase():
    """Test Supabase Storage connection"""
    print("\n📦 Testing Supabase Storage...")
    try:
        from supabase_storage_client import get_supabase
        supabase = get_supabase()
        
        # Try to list buckets
        buckets = supabase.storage.list_buckets()
        
        print("   ✅ Supabase Storage: CONNECTED")
        print(f"      Available buckets: {[b.name for b in buckets]}")
        
        # Check if required buckets exist
        bucket_names = [b.name for b in buckets]
        if 'tracks' not in bucket_names:
            print("   ⚠️  Warning: 'tracks' bucket not found. Please create it in Supabase.")
        if 'covers' not in bucket_names:
            print("   ⚠️  Warning: 'covers' bucket not found. Please create it in Supabase.")
        
        return True
    except Exception as e:
        print(f"   ❌ Supabase Storage: ERROR")
        print(f"      Error: {e}")
        print("\n      Solution:")
        print("      1. Check SUPABASE_URL and SUPABASE_KEY in .env")
        print("      2. Make sure you have created 'tracks' and 'covers' buckets")
        print("      3. Set buckets to Public")
        return False

def test_env():
    """Test environment variables"""
    print("\n📋 Testing Environment Variables...")
    
    required_vars = [
        "FIREBASE_CREDENTIALS_PATH",
        "FIREBASE_DATABASE_URL",
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "ADMIN_EMAIL",
        "ADMIN_PASSWORD"
    ]
    
    all_present = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if "KEY" in var or "PASSWORD" in var or "SECRET" in var:
                print(f"   ✅ {var}: Set (hidden)")
            else:
                print(f"   ✅ {var}: {value[:50]}...")
        else:
            print(f"   ❌ {var}: NOT SET")
            all_present = False
    
    return all_present

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 DGT-SOUNDS - Connection Test")
    print("="*60)
    
    env_ok = test_env()
    firebase_ok = test_firebase()
    supabase_ok = test_supabase()
    
    print("\n" + "="*60)
    print("📊 Test Results:")
    print("="*60)
    print(f"   Environment Variables: {'✅ OK' if env_ok else '❌ ISSUES'}")
    print(f"   Firebase Firestore:    {'✅ OK' if firebase_ok else '❌ ISSUES'}")
    print(f"   Supabase Storage:      {'✅ OK' if supabase_ok else '❌ ISSUES'}")
    print("="*60)
    
    if env_ok and firebase_ok and supabase_ok:
        print("\n🎉 All connections are working!")
        print("\n🚀 Next steps:")
        print("   1. Run: python setup_database.py (to add sample data)")
        print("   2. Run: python main.py (to start the server)")
        print("   3. Open: http://localhost:8000/docs (API documentation)")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\n📖 Check README.md for setup instructions.")
    
    print()

if __name__ == "__main__":
    main()
