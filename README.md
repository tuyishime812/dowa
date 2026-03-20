# DGT-SOUNDS - Music Streaming Platform

A modern music streaming website built with FastAPI backend and Supabase database.

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
- **Supabase** - PostgreSQL database and storage
- **Uvicorn** - ASGI server
- **Python-dotenv** - Environment variables

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with CSS variables
- **JavaScript (ES6+)** - Vanilla JavaScript
- **Font Awesome** - Icons

## Prerequisites

- Python 3.9+
- Node.js (optional, for frontend development)
- Supabase account (free tier available)

## Setup Instructions

### 1. Clone/Download the Project

Navigate to the project directory:
```bash
cd C:\Users\Student.LAPTOP-46MOQA5A\Desktop\projects\dowa
```

### 2. Set Up Supabase

1. Go to [Supabase](https://supabase.com) and create a free account
2. Create a new project
3. Go to the SQL Editor in your Supabase dashboard
4. Copy and paste the contents of `backend/supabase_schema.sql`
5. Run the SQL to create tables and sample data

### 3. Configure Backend

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

4. Update the `.env` file with your Supabase credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

5. Start the backend server:
```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 4. Set Up Frontend

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
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── .env.example            # Example environment file
│   ├── supabase_schema.sql     # Database schema
│   └── uploads/                # Uploaded files (auto-created)
│       ├── tracks/             # Audio files
│       └── covers/             # Cover art
├── frontend/
│   ├── index.html              # Main HTML file
│   └── assets/
│       ├── css/
│       │   └── style.css       # Stylesheet
│       ├── js/
│       │   └── app.js          # JavaScript application
│       └── images/
│           └── logo.png        # Logo image
├── dowa_logo.png               # Original logo
└── README.md                   # This file
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
- Verify `.env` file has correct Supabase credentials

### Frontend can't connect to API
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify API_BASE_URL in `frontend/assets/js/app.js`

### Database errors
- Run the SQL schema in Supabase SQL Editor
- Check if Supabase project is active
- Verify SUPABASE_KEY has correct permissions

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
2. Set environment variables
3. Deploy from GitHub

### Frontend (Netlify/Vercel)
1. Upload the `frontend` folder
2. Configure build settings (none needed for static site)
3. Update API_BASE_URL to production URL

## License

This project is open source and available under the MIT License.

## Support

For issues and feature requests, please create an issue in the repository.

---

**DGT-SOUNDS** - Your ultimate destination for the hottest tracks 🎵
