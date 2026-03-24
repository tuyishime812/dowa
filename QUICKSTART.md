# DGT-SOUNDS - Quick Start Guide

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example env file
copy .env.example .env  # Windows
# or cp .env.example .env  # Mac/Linux

# Edit .env with your Firebase and Supabase credentials
```

### 3. Add Firebase Credentials
- Download `firebase_credentials.json` from Firebase Console
- Place it in the `backend/` folder

### 4. Test Connections (Optional but Recommended)
```bash
cd backend
python test_connections.py
```
This will verify that Firebase and Supabase are configured correctly.

### 5. Add Sample Data (Optional)
```bash
python setup_database.py
```
This creates sample artists, albums, and tracks in your database.

### 6. Start Servers

**Backend:**
```bash
python main.py
```

**Frontend (new terminal):**
```bash
cd ../frontend
python -m http.server 3000
```

---

## 🔗 Access URLs

| Service | URL |
|---------|-----|
| **Main Site** | http://localhost:3000 |
| **Admin Dashboard** | http://localhost:3000/admin/index.html |
| **Backend API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

---

## 🔐 Admin Login

**Default Credentials:**
- Email: `admin@dgt-sounds.com`
- Password: `admin123`

---

## 📋 Required Setup

### Firebase Firestore
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable **Firestore Database**
4. Go to **Project Settings** → **Service accounts**
5. Click **Generate new private key**
6. Save as `firebase_credentials.json` in `backend/` folder

### Supabase Storage
1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Go to **Storage** → Create two buckets:
   - **Bucket 1:** `tracks` (Public) - for audio files
   - **Bucket 2:** `covers` (Public) - for images
4. Go to **SQL Editor** → Run the SQL from `backend/supabase_policies.sql`
5. Go to **Settings** → **API**
6. Copy your **Project URL** and **anon key**

### Update .env File
```env
# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase_credentials.json
FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com

# Supabase Storage
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

---

## 🎯 Quick Actions

### Upload a Track
1. Click "Upload" in admin sidebar
2. Fill in track details (Title, Artist, Album, Genre)
3. Drag audio file or click to browse
4. Add cover art (optional)
5. Click "Upload Track"

### Edit a Track
1. Go to "Tracks" page
2. Click the edit (pencil) icon
3. Modify details
4. Click "Save Changes"

### Delete a Track
1. Go to "Tracks" page
2. Click the delete (trash) icon
3. Confirm deletion

---

## ⌨️ Keyboard Shortcuts (Main Site)

| Key | Action |
|-----|--------|
| `Space` | Play/Pause |
| `←` | Previous track |
| `→` | Next track |
| `↑` | Volume up |
| `↓` | Volume down |

---

## 🛠️ Configuration

### Change Admin Password
Edit `backend/.env`:
```env
ADMIN_PASSWORD=your_new_password
```
Then restart the backend server.

---

## 📁 File Structure

```
dowa/
├── backend/
│   ├── main.py                    # FastAPI server
│   ├── firebase_client.py         # Firebase client
│   ├── supabase_storage_client.py # Supabase Storage client
│   ├── .env                       # Configuration
│   ├── requirements.txt           # Dependencies
│   └── firebase_credentials.json  # (do not commit!)
│
├── frontend/
│   ├── index.html           # Main site
│   ├── admin/
│   │   └── index.html       # Admin dashboard
│   └── assets/
│       ├── css/
│       ├── js/
│       └── images/
│
└── README.md
```

---

## 🔧 Troubleshooting

### Backend not starting?
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Firebase credentials error?
- Ensure `firebase_credentials.json` exists in `backend/` folder
- Verify file is valid JSON from Firebase Console

### Supabase Storage upload error?
- Check SUPABASE_URL and SUPABASE_KEY in `.env`
- Verify buckets `tracks` and `covers` exist
- Ensure buckets are set to **Public**

### Can't login to admin?
- Check backend is running
- Use default credentials: admin@dgt-sounds.com / admin123
- Clear browser cache

---

## 📞 Need Help?

Check the full [README.md](README.md) or [FIRESTORE_SCHEMA.md](backend/FIRESTORE_SCHEMA.md) for detailed documentation.

**Enjoy DGT-SOUNDS! 🎵**
