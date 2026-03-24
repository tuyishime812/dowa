"""
Firebase Database Client
Initialize and provide Firestore database access
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

_db = None

def get_firebase_app():
    """Get or initialize Firebase app"""
    try:
        app = firebase_admin.get_app()
        return app
    except ValueError:
        credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase_credentials.json")
        
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(
                f"Firebase credentials file not found at {credentials_path}. "
                "Please download the service account JSON from Firebase Console."
            )
        
        cred = credentials.Certificate(credentials_path)
        app = firebase_admin.initialize_app(cred)
        return app

def get_db():
    """Get Firestore database client"""
    global _db
    if _db is None:
        get_firebase_app()
        _db = firestore.client()
    return _db
