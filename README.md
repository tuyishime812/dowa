# DGT-SOUNDS - Music Streaming Platform

A modern music streaming website built with FastAPI backend, Firebase Firestore database, and Supabase Storage.

![DGT-SOUNDS](frontend/assets/images/logo.png)

## Features

### User Features
- 🎵 **Music Streaming** - Play, pause, skip tracks with a beautiful player
- 🔍 **Search** - Search tracks by title, artist, or album
- 📁 **Genres** - Browse music by genre categories
- 👨‍🎤 **Artists** - View and explore artists
- 📤 **Upload** - Upload your own tracks with cover art
- 📱 **Responsive** - Works on desktop, tablet, and mobile

### Admin Dashboard Features
- 🔐 **Secure Login** - Admin authentication system
- 📊 **Analytics Dashboard** - View total tracks, albums, artists, and plays
- 🎶 **Track Management** - Upload, edit, delete tracks
- 💿 **Album Management** - Create and manage albums
- 👥 **Artist Management** - Add and edit artist information
- 🔍 **Search & Filter** - Easy content management with search
- 📱 **Fully Responsive** - Admin panel works on all devices

## Accessing the Admin Dashboard

1. Go to http://localhost:3000/admin/index.html
2. Login with default credentials:
   - **Email:** admin@dgt-sounds.com
   - **Password:** admin123
3. Or click "Admin Dashboard" link in the footer of the main site

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Firebase Firestore** - NoSQL database
- **Supabase Storage** - Object storage for audio files and images
- **Uvicorn** - ASGI server
- **Python-dotenv** - Environment variables

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with CSS variables
- **JavaScript (ES6+)** - Vanilla JavaScript
- **Font Awesome** - Icons

## Prerequisites

- Python 3.9+
- Firebase account (free tier available)
- Supabase account (free tier available)

## Setup Instructions

### 1. Clone/Download the Project

Navigate to the project directory:
```bash
cd C:\Users\Student.LAPTOP-46MOQA5A\Desktop\projects\dowa
```

### 2. Set Up Firebase Firestore

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project (e.g., "DGT-SOUNDS")
3. Enable **Firestore Database** in the left sidebar
4. Start in **production mode** (you can update security rules later)
5. Go to **Project Settings** (gear icon ⚙️) → **Service accounts**
6. Click **Generate new private key**
7. Save the JSON file as `firebase_credentials.json` in the `backend/` folder

### 3. Set Up Supabase Storage

1. Go to [Supabase](https://supabase.com)
2. Create a new project (or use existing one)
3. Go to **Storage** in the left sidebar
4. Create two buckets:
   - **Bucket 1:** `tracks` (for audio files) - Set to **Public**
   - **Bucket 2:** `covers` (for images) - Set to **Public**
5. Go to **SQL Editor** and run the SQL from `backend/supabase_policies.sql`
   - This adds the necessary policies for file upload/download
6. Go to **Settings** → **API**
7. Copy your **Project URL** and **anon/public key**

### 4. Configure Backend

1. Navigate to the backend folder:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and update it:
```bash
copy .env.example .env  # Windows
# or
cp .env.example .env  # Mac/Linux
```

5. Update the `.env` file with your credentials:
```env
# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=./firebase_credentials.json
FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com

# Supabase Storage Configuration
SUPABASE_URL=https://your-project.supabase.co
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

6. Start the backend server:
```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 5. Set Up Frontend

1. Open `frontend/index.html` in your web browser
2. Or use a simple HTTP server:

```bash
cd frontend
python -m http.server 3000
```

Then open `http://localhost:3000` in your browser.

## Project Structure

```
dowa/
├── backend/
│   ├── main.py                      # FastAPI application
│   ├── firebase_client.py           # Firebase Firestore client
│   ├── supabase_storage_client.py   # Supabase Storage client
│   ├── setup_database.py            # Database setup script (sample data)
│   ├── test_connections.py          # Connection test script
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment variables
│   ├── .env.example                 # Example environment file
│   ├── firebase_credentials.json    # Firebase service account (do not commit!)
│   └── FIRESTORE_SCHEMA.md          # Database schema documentation
├── frontend/
│   ├── index.html                   # Main HTML file
│   ├── admin/
│   │   └── index.html               # Admin dashboard
│   └── assets/
│       ├── css/
│       │   ├── style.css            # Main styles
│       │   └── admin.css            # Admin styles
│       ├── js/
│       │   ├── app.js               # Main application
│       │   └── admin.js             # Admin application
│       └── images/
│           └── logo.png             # Logo image
├── .gitignore                       # Git ignore file
├── SETUP_GUIDE.md                   # Complete setup guide
├── QUICKSTART.md                    # Quick start guide
├── dowa_logo.png                    # Original logo
└── README.md                        # This file
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tracks` | Get all tracks |
| GET | `/api/tracks/{id}` | Get single track |
| POST | `/api/tracks` | Upload new track |
| DELETE | `/api/tracks/{id}` | Delete track |
| GET | `/api/artists` | Get all artists |
| GET | `/api/albums` | Get all albums |
| GET | `/api/genres` | Get all genres |
| GET | `/api/search?q=query` | Search tracks |
| GET | `/api/featured` | Get featured tracks |
| GET | `/api/latest` | Get latest tracks |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Space | Play/Pause |
| ← | Previous track |
| → | Next track |
| ↑ | Volume up |
| ↓ | Volume down |

## Supabase Storage Setup

### Create Buckets

In Supabase Dashboard → Storage:

1. Click **New bucket**
2. **Bucket name:** `tracks`
3. **Public bucket:** ✅ Yes
4. Click **Create bucket**

Repeat for covers:
1. Click **New bucket**
2. **Bucket name:** `covers`
3. **Public bucket:** ✅ Yes
4. Click **Create bucket**

### Storage Security Rules

For production, add these policies in Supabase → Storage → Policies:

**For `tracks` bucket:**
```sql
-- Allow public read access
CREATE POLICY "Public Read Access" ON storage.objects
FOR SELECT USING (bucket_id = 'tracks');

-- Allow authenticated upload
CREATE POLICY "Authenticated Upload" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'tracks');

-- Allow delete
CREATE POLICY "Allow Delete" ON storage.objects
FOR DELETE USING (bucket_id = 'tracks');
```

**For `covers` bucket:**
```sql
-- Allow public read access
CREATE POLICY "Public Read Access" ON storage.objects
FOR SELECT USING (bucket_id = 'covers');

-- Allow authenticated upload
CREATE POLICY "Authenticated Upload" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'covers');

-- Allow delete
CREATE POLICY "Allow Delete" ON storage.objects
FOR DELETE USING (bucket_id = 'covers');
```

## Firestore Security Rules

For production, update your Firestore security rules in Firebase Console:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /tracks/{trackId} {
      allow read: if true;
      allow create, update, delete: if request.auth != null;
    }
    match /artists/{artistId} {
      allow read: if true;
      allow create, update, delete: if request.auth != null;
    }
    match /albums/{albumId} {
      allow read: if true;
      allow create, update, delete: if request.auth != null;
    }
  }
}
```

## Customization

### Colors
Edit the CSS variables in `frontend/assets/css/style.css`:

```css
:root {
    --primary-color: #ff6b00;      /* Main brand color */
    --primary-hover: #ff8533;      /* Hover state */
    --bg-dark: #0f0f1a;            /* Background */
    --bg-card: #16162a;            /* Card background */
}
```

### Logo
Replace `frontend/assets/images/logo.png` with your own logo.

## Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check if port 8000 is available
- Verify `firebase_credentials.json` exists in the backend folder
- Check `.env` file has correct Supabase credentials

### Frontend can't connect to API
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify API_BASE_URL in `frontend/assets/js/app.js`

### Firebase connection errors
- Verify `firebase_credentials.json` is in the backend folder
- Check Firebase project is active
- Ensure Firestore database is enabled

### Supabase Storage upload errors
- Verify SUPABASE_URL and SUPABASE_KEY in `.env`
- Check buckets `tracks` and `covers` exist
- Ensure buckets are set to **Public**
- Verify storage policies allow read/write access

## Development

### Running in Development

Backend with auto-reload:
```bash
cd backend
uvicorn main:app --reload
```

Frontend with live server (if using VS Code):
- Install "Live Server" extension
- Right-click `index.html` and select "Open with Live Server"

## Deployment

### Backend (Railway/Render/Heroku)
1. Create a new Python project
2. Set environment variables (Firebase credentials, Supabase credentials)
3. Upload `firebase_credentials.json` securely
4. Deploy from GitHub

### Frontend (Netlify/Vercel)
1. Upload the `frontend` folder
2. Configure build settings (none needed for static site)
3. Update API_BASE_URL to production URL

## Cost Considerations

### Firebase Firestore (Free Tier)
- 50,000 reads/day
- 20,000 writes/day
- 1 GB storage

### Supabase Storage (Free Tier)
- 1 GB file storage
- 2 GB bandwidth/month
- Unlimited API requests

## License

This project is open source and available under the MIT License.

## Support

For issues and feature requests, please create an issue in the repository.

---

**DGT-SOUNDS** - Your ultimate destination for the hottest tracks 🎵
