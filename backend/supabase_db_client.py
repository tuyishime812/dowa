"""
Supabase Database Client
PostgreSQL database connection and operations
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

_supabase = None

def get_supabase():
    """Get Supabase client (database + storage)"""
    global _supabase
    if _supabase is None:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not all([supabase_url, supabase_key]):
            raise ValueError(
                "Missing Supabase credentials. "
                "Please set SUPABASE_URL and SUPABASE_KEY in your .env file."
            )

        _supabase = create_client(supabase_url, supabase_key)

    return _supabase

def get_db():
    """Get Supabase client for database operations"""
    return get_supabase()
