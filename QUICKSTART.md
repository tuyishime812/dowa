# DGT-SOUNDS - Quick Start Guide

## 🚀 Servers Running

| Service | URL | Status |
|---------|-----|--------|
| **Main Site** | http://localhost:3000 | ✅ Running |
| **Admin Dashboard** | http://localhost:3000/admin/index.html | ✅ Running |
| **Backend API** | http://localhost:8000 | ✅ Running |
| **API Docs** | http://localhost:8000/docs | ✅ Running |

---

## 🔐 Admin Login

**Default Credentials:**
- Email: `admin@dgt-sounds.com`
- Password: `admin123`

---

## 📋 Admin Dashboard Features

### Dashboard (Home)
- View total tracks, albums, artists, and plays
- See top 5 trending tracks
- View recent uploads

### Tracks Management
- View all tracks in a table
- Search and filter by genre
- Edit track details (title, artist, album, genre)
- Delete tracks
- Play preview

### Upload Page
- Drag & drop audio files
- Upload cover art
- Fill in track metadata
- Support for MP3, WAV, FLAC

### Albums Management
- View all albums in grid
- Add new albums
- Edit album details
- Delete albums

### Artists Management
- View all artists
- Add new artists
- Edit artist info and images
- Delete artists

---

## 🎯 Quick Actions

### Upload a Track
1. Click "Upload" in sidebar
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

### Connect Supabase
1. Create account at https://supabase.com
2. Create new project
3. Run SQL from `backend/supabase_schema.sql`
4. Update `backend/.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

---

## 📁 File Structure

```
dowa/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── .env                 # Configuration
│   ├── requirements.txt     # Dependencies
│   └── uploads/             # Uploaded files
│
├── frontend/
│   ├── index.html           # Main site
│   ├── admin/
│   │   └── index.html       # Admin dashboard
│   └── assets/
│       ├── css/
│       │   ├── style.css    # Main styles
│       │   └── admin.css    # Admin styles
│       ├── js/
│       │   ├── app.js       # Main site JS
│       │   └── admin.js     # Admin JS
│       └── images/
│           └── logo.png
│
└── README.md
```

---

## 🔧 Troubleshooting

### Backend not starting?
```bash
cd backend
venv\Scripts\activate
python main.py
```

### Can't login to admin?
- Check backend is running
- Use default credentials: admin@dgt-sounds.com / admin123
- Clear browser cache

### Upload not working?
- Ensure backend is running
- Check file size (max depends on server config)
- Supported formats: MP3, WAV, FLAC for audio; JPG, PNG for images

---

## 📞 Need Help?

Check the full README.md for detailed documentation.

**Enjoy DGT-SOUNDS! 🎵**
