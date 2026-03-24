# DGT-SOUNDS - Complete Setup Guide

This guide will walk you through setting up the entire DGT-SOUNDS platform from scratch.

---

## 📋 Prerequisites

- Python 3.9 or higher
- Google account (for Firebase)
- Email address (for Supabase)

---

## Step 1: Set Up Firebase Firestore (Database)

### 1.1 Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click **"Add project"** or **"Create a project"**
3. **Project name:** `DGT-SOUNDS` (or your preferred name)
4. Click **Continue**
5. **Google Analytics:** Toggle OFF (optional)
6. Click **Create project**
7. Wait for creation → Click **Continue**

### 1.2 Enable Firestore Database
1. In left sidebar → **Build** → **Firestore Database**
2. Click **Create database**
3. **Security rules:** Start in **production mode**
4. Click **Next**
5. **Location:** Choose closest to you (e.g., `us-central`)
6. Click **Enable**

### 1.3 Download Service Account Credentials
1. Click **⚙️ Settings** (gear icon at bottom of left sidebar)
2. Click **Project settings**
3. Go to **Service accounts** tab
4. Click **Generate new private key**
5. Click **Generate key** in popup
6. A JSON file downloads (e.g., `dgt-sounds-firebase-adminsdk-xxxxx.json`)
7. **Rename** it to: `firebase_credentials.json`
8. **Move** it to: `backend/` folder

---

## Step 2: Set Up Supabase Storage (File Storage)

### 2.1 Create Supabase Account
1. Go to https://supabase.com
2. Click **Start your project** or **Sign In**
3. Sign up with GitHub or email

### 2.2 Create a New Project
1. Click **New Project**
2. **Organization:** Select or create
3. **Project name:** `DGT-SOUNDS`
4. **Database password:** Create a strong password (save it!)
5. **Region:** Choose closest to you
6. Click **Create new project**
7. Wait 2-3 minutes for setup

### 2.3 Create Storage Buckets
1. In left sidebar → **Storage**
2. Click **New bucket**
3. **Bucket name:** `tracks`
4. **Public bucket:** ✅ **Yes** (toggle on)
5. Click **Create bucket**

6. Click **New bucket** again
7. **Bucket name:** `covers`
8. **Public bucket:** ✅ **Yes** (toggle on)
9. Click **Create bucket**

### 2.4 Get API Credentials
1. In left sidebar → **Settings** (gear icon at bottom)
2. Click **API**
3. Copy these two values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (long string under `service_role`)

---

## Step 3: Configure the Backend

### 3.1 Navigate to Backend Folder
```bash
cd c:\Users\Student.LAPTOP-46MOQA5A\Desktop\projects\dowa\backend
```

### 3.2 Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3.3 Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Firebase Admin SDK
- Supabase client
- Uvicorn (server)
- Other utilities

### 3.4 Configure Environment Variables
```bash
copy .env.example .env
```

Open `.env` in a text editor and update:

```env
# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=./firebase_credentials.json
FIREBASE_DATABASE_URL=https://kio-d02c0.firebaseio.com

# Supabase Storage Configuration
SUPABASE_URL=https://YOUR-PROJECT.supabase.co
SUPABASE_KEY=your-anon-key-here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080

# Admin Credentials
ADMIN_EMAIL=admin@dgt-sounds.com
ADMIN_PASSWORD=admin123
```

**Replace:**
- `SUPABASE_URL` with your Supabase project URL
- `SUPABASE_KEY` with your Supabase anon key

---

## Step 4: Test Connections

Run the test script to verify everything is configured correctly:

```bash
python test_connections.py
```

**Expected output:**
```
🔥 Testing Firebase Firestore...
   ✅ Firebase Firestore: CONNECTED

📦 Testing Supabase Storage...
   ✅ Supabase Storage: CONNECTED
      Available buckets: ['tracks', 'covers']

📊 Test Results:
   ✅ All connections are working!
```

**If you see errors:**
- Check that `firebase_credentials.json` exists in the backend folder
- Verify `.env` has correct Supabase credentials
- Make sure Supabase buckets are set to **Public**

---

## Step 5: Add Sample Data (Optional)

Add sample artists, albums, and tracks to your database:

```bash
python setup_database.py
```

This creates:
- 5 sample artists
- 4 sample albums
- 5 sample tracks (with placeholder URLs)

---

## Step 6: Start the Backend Server

```bash
python main.py
```

**Expected output:**
```
🚀 Starting DGT-SOUNDS API...
✅ Firebase Firestore connected
✅ Supabase Storage connected
🎵 API ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The API is now running at: **http://localhost:8000**

**API Documentation:** http://localhost:8000/docs

---

## Step 7: Start the Frontend

Open a **new terminal** window:

```bash
cd c:\Users\Student.LAPTOP-46MOQA5A\Desktop\projects\dowa\frontend
python -m http.server 3000
```

The website is now running at: **http://localhost:3000**

**Admin Dashboard:** http://localhost:3000/admin/index.html

---

## 🎉 You're Done!

### Access Your Application

| Service | URL | Status |
|---------|-----|--------|
| **Main Website** | http://localhost:3000 | ✅ |
| **Admin Dashboard** | http://localhost:3000/admin | ✅ |
| **Backend API** | http://localhost:8000 | ✅ |
| **API Docs** | http://localhost:8000/docs | ✅ |

### Admin Login
- **Email:** `admin@dgt-sounds.com`
- **Password:** `admin123`

---

## 🔧 Troubleshooting

### Backend won't start

**Error: `firebase_credentials.json` not found**
```
Solution: Download from Firebase Console → Project Settings → Service accounts
```

**Error: `Missing Supabase credentials`**
```
Solution: Check .env file has correct SUPABASE_URL and SUPABASE_KEY
```

**Error: `Port 8000 already in use`**
```bash
# Change port in .env:
PORT=8001

# Or kill the process using port 8000:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend can't connect to API

1. Make sure backend is running: http://localhost:8000
2. Check browser console for errors
3. Verify CORS settings in `.env`

### Supabase upload fails

1. Check buckets exist: `tracks` and `covers`
2. Verify buckets are **Public** (in Supabase Storage settings)
3. Check API key has correct permissions

### Firebase connection fails

1. Verify `firebase_credentials.json` is in backend folder
2. Check file is valid JSON (open in text editor)
3. Ensure Firestore is enabled in Firebase Console

---

## 📚 Next Steps

1. **Upload Your First Track:**
   - Go to Admin Dashboard
   - Click "Upload" in sidebar
   - Fill in track details and upload audio file

2. **Customize the Site:**
   - Edit colors in `frontend/assets/css/style.css`
   - Replace logo in `frontend/assets/images/logo.png`

3. **Deploy to Production:**
   - Backend: Railway, Render, or Heroku
   - Frontend: Netlify or Vercel
   - See README.md for deployment guide

---

## 📞 Need Help?

- **Full Documentation:** [README.md](README.md)
- **Database Schema:** [backend/FIRESTORE_SCHEMA.md](backend/FIRESTORE_SCHEMA.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)

**Enjoy DGT-SOUNDS! 🎵**
