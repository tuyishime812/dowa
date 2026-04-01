"""
DGT-SOUNDS Backend API - Vercel Serverless Function
FastAPI backend adapted for Vercel serverless
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the FastAPI app
from backend.main import app

# Export for Vercel
handler = app
