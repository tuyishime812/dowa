"""
Supabase Storage Client
Handle file uploads and retrieval using Supabase Storage buckets
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

_supabase = None

def get_supabase():
    """Get Supabase client"""
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

def upload_file(file_bytes: bytes, bucket: str, file_path: str, content_type: str = "application/octet-stream"):
    """
    Upload a file to Supabase Storage
    
    Args:
        file_bytes: File content as bytes
        bucket: The storage bucket name
        file_path: The path to store the file under
        content_type: MIME type of the file
    
    Returns:
        str: Public URL of the uploaded file
    """
    supabase = get_supabase()
    
    # Upload file
    supabase.storage.from_(bucket).upload(
        file_path,
        file_bytes,
        {"content-type": content_type, "upsert": "true"}
    )
    
    # Get public URL
    public_url = supabase.storage.from_(bucket).get_public_url(file_path)
    
    # Return the URL directly (get_public_url returns a string)
    return public_url

def delete_file(bucket: str, file_path: str):
    """
    Delete a file from Supabase Storage
    
    Args:
        bucket: The storage bucket name
        file_path: The path of the file to delete
    """
    supabase = get_supabase()
    supabase.storage.from_(bucket).remove([file_path])

def get_file_url(bucket: str, file_path: str) -> str:
    """
    Get the public URL for a file
    
    Args:
        bucket: The storage bucket name
        file_path: The path of the file
    
    Returns:
        str: Public URL of the file
    """
    supabase = get_supabase()
    response = supabase.storage.from_(bucket).get_public_url(file_path)
    return response.url
