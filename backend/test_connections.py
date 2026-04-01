"""
Test Connections Script
Verify Supabase database and storage connections
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_supabase_db():
    """Test Supabase Database connection"""
    print("\n🗄️  Testing Supabase Database...")
    try:
        from supabase_db_client import get_db
        supabase = get_db()
        
        # Try to query the tracks table
        result = supabase.table("tracks").select("id").limit(1).execute()
        
        print("   ✅ Supabase Database: CONNECTED")
        return True
    except Exception as e:
        print(f"   ❌ Supabase Database: ERROR")
        print(f"      Error: {e}")
        print("\n      Solution:")
        print("      1. Check SUPABASE_URL and SUPABASE_KEY in .env")
        print("      2. Run supabase_schema.sql in Supabase SQL Editor")
        return False

def test_supabase_storage():
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
                print(f"   ✅ {var}: {value}")
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
    db_ok = test_supabase_db()
    storage_ok = test_supabase_storage()

    print("\n" + "="*60)
    print("📊 Test Results:")
    print("="*60)
    print(f"   Environment Variables: {'✅ OK' if env_ok else '❌ ISSUES'}")
    print(f"   Supabase Database:     {'✅ OK' if db_ok else '❌ ISSUES'}")
    print(f"   Supabase Storage:      {'✅ OK' if storage_ok else '❌ ISSUES'}")
    print("="*60)

    if env_ok and db_ok and storage_ok:
        print("\n🎉 All connections are working!")
        print("\n🚀 Next steps:")
        print("   1. Run: python main.py (to start the server)")
        print("   2. Open: http://localhost:8000/docs (API documentation)")
        print("   3. Access: http://localhost:3000 (frontend)")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\n📖 Check README.md for setup instructions.")

    print()

if __name__ == "__main__":
    main()
