# 🚀 DGT-SOUNDS Deployment Guide

Complete guide to deploy your music streaming platform to production.

---

## 📋 Overview

| Component | Recommended Service | Alternative |
|-----------|-------------------|-------------|
| **Backend** | Railway | Render, Heroku |
| **Frontend** | Netlify | Vercel, Cloudflare Pages |
| **Database** | Supabase PostgreSQL | (already configured) |
| **Storage** | Supabase Storage | (already configured) |

---

## 🎯 Prerequisites

Before deploying, ensure you have:

- ✅ [GitHub account](https://github.com)
- ✅ [Supabase account](https://supabase.com) (free tier available)
- ✅ [Railway account](https://railway.app) (free trial available)
- ✅ [Netlify account](https://netlify.com) (free tier available)

---

## 📦 Step 1: Prepare Your Repository

### 1.1 Push all changes to GitHub

```bash
git push origin main
```

✅ Already done! Your code is on GitHub.

### 1.2 Update `.env.example` for production

Your `.env.example` is already good. Make sure your production `.env` has:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Settings (update with production URLs)
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Admin Credentials (change for production!)
ADMIN_EMAIL=admin@dgt-sounds.com
ADMIN_PASSWORD=CHANGE_THIS_PASSWORD
```

---

## 🗄️ Step 2: Set Up Supabase (Database + Storage)

### 2.1 Create Supabase Project

1. Go to [Supabase](https://supabase.com)
2. Click **"New Project"**
3. Fill in:
   - **Name:** DGT-SOUNDS
   - **Database Password:** (save this securely)
   - **Region:** Choose closest to your users
4. Click **"Create new project"**

### 2.2 Run Database Schema

1. Go to **SQL Editor** in Supabase dashboard
2. Click **"New Query"**
3. Copy and paste contents from `backend/supabase_schema.sql`
4. Click **"Run"**

✅ This creates:
- `tracks` table
- `artists` table
- `albums` table
- Indexes for performance

### 2.3 Create Storage Buckets

The SQL script already creates buckets, but verify:

1. Go to **Storage** in Supabase dashboard
2. You should see:
   - `tracks` bucket (public)
   - `covers` bucket (public)

If not created manually:
- Click **"New bucket"**
- Name: `tracks`, Public: ✅
- Click **"New bucket"**
- Name: `covers`, Public: ✅

### 2.4 Get API Credentials

1. Go to **Settings** → **API**
2. Copy:
   - **Project URL:** `https://xxxxx.supabase.co`
   - **anon/public key:** `eyJhbG...`

You'll need these for backend and frontend.

---

## 🔧 Step 3: Deploy Backend (Railway)

### 3.1 Connect GitHub to Railway

1. Go to [Railway](https://railway.app)
2. Click **"Login"** → **"Sign in with GitHub"**
3. Authorize Railway

### 3.2 Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `dowa`
4. Railway will auto-detect it's a Python project

### 3.3 Configure Service

1. Click on your service
2. Go to **"Settings"** tab
3. Set **Root Directory:** `backend`
4. Set **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3.4 Add Environment Variables

In Railway dashboard → **Variables** → **"Add Variable"**:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://your-domain.netlify.app,https://your-custom-domain.com
ADMIN_EMAIL=admin@dgt-sounds.com
ADMIN_PASSWORD=your-secure-password
```

### 3.5 Deploy

1. Railway will auto-deploy after you add variables
2. Go to **"Deployments"** tab to watch progress
3. Once deployed, copy your **Public URL** (e.g., `https://dowa-production.up.railway.app`)

### 3.6 Test Backend

```bash
curl https://your-railway-url.up.railway.app/api/health
```

Should return: `{"status": "healthy", "message": "DGT-SOUNDS API is running"}`

---

## 🎨 Step 4: Deploy Frontend (Netlify)

### 4.1 Prepare Frontend

Update the API URL in `frontend/assets/js/app.js`:

```javascript
// Change this line:
const API_BASE_URL = 'http://localhost:8000';

// To your Railway backend URL:
const API_BASE_URL = 'https://your-railway-url.up.railway.app';
```

Or use environment variable (better):

```javascript
const API_BASE_URL = window.API_BASE_URL || 'http://localhost:8000';
```

Then add to `frontend/index.html` before the script:

```html
<script>
    window.API_BASE_URL = 'https://your-railway-url.up.railway.app';
</script>
<script src="assets/js/app.js"></script>
```

### 4.2 Deploy to Netlify

#### Option A: Deploy via GitHub (Recommended)

1. Go to [Netlify](https://netlify.com)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect to GitHub
4. Choose your repository: `dowa`
5. Configure build settings:
   - **Base directory:** `frontend`
   - **Publish directory:** `frontend`
   - **Build command:** (leave empty - it's static)
6. Click **"Deploy site"**

#### Option B: Drag & Drop (Quick Test)

1. Go to [Netlify Drop](https://app.netlify.com/drop)
2. Drag and drop the `frontend` folder
3. Site will be deployed instantly

### 4.3 Configure Environment Variables (Netlify)

If using Option A:

1. Go to **Site settings** → **Environment variables**
2. Add:
   - Key: `API_BASE_URL`
   - Value: `https://your-railway-url.up.railway.app`

### 4.4 Update CORS on Backend

Add your Netlify URL to allowed origins in Railway:

```
ALLOWED_ORIGINS=https://your-site.netlify.app,https://your-custom-domain.com
```

Redeploy backend after updating.

---

## 🌐 Step 5: Custom Domain (Optional)

### 5.1 Frontend Domain (Netlify)

1. Go to **Domain settings** in Netlify
2. Click **"Add custom domain"**
3. Enter your domain (e.g., `www.dgt-sounds.com`)
4. Follow DNS configuration instructions

### 5.2 Backend Domain (Railway)

1. Go to **Settings** → **Domains**
2. Click **"Add Domain"**
3. Enter your domain (e.g., `api.dgt-sounds.com`)
4. Update DNS records as instructed

---

## 🔐 Step 6: Security Hardening

### 6.1 Update Firestore/Supabase Rules

**Supabase Database:**

In Supabase → **Authentication** → **Policies**:

```sql
-- Enable RLS on all tables
ALTER TABLE tracks ENABLE ROW LEVEL SECURITY;
ALTER TABLE artists ENABLE ROW LEVEL SECURITY;
ALTER TABLE albums ENABLE ROW LEVEL SECURITY;

-- Allow public read access
CREATE POLICY "Public Read Tracks" ON tracks
FOR SELECT USING (true);

CREATE POLICY "Public Read Artists" ON artists
FOR SELECT USING (true);

CREATE POLICY "Public Read Albums" ON albums
FOR SELECT USING (true);

-- Allow authenticated admin to write
CREATE POLICY "Admin Write Tracks" ON tracks
FOR ALL USING (
    EXISTS (
        SELECT 1 FROM admin_users 
        WHERE admin_users.email = auth.jwt()->>'email'
    )
);
```

### 6.2 Update Storage Policies

In Supabase → **Storage** → **Policies**:

**For `tracks` bucket:**
```sql
-- Public read
CREATE POLICY "Public Read" ON storage.objects
FOR SELECT USING (bucket_id = 'tracks');

-- Authenticated upload only
CREATE POLICY "Authenticated Upload" ON storage.objects
FOR INSERT WITH CHECK (
    bucket_id = 'tracks' 
    AND auth.role() = 'authenticated'
);

-- Admin delete
CREATE POLICY "Admin Delete" ON storage.objects
FOR DELETE USING (
    bucket_id = 'tracks'
    AND auth.role() = 'authenticated'
);
```

**For `covers` bucket:**
```sql
-- Same as tracks but with bucket_id = 'covers'
```

### 6.3 Change Admin Password

Update in Railway environment variables:

```
ADMIN_PASSWORD=your-new-secure-password
```

---

## ✅ Step 7: Testing Checklist

### Backend Tests

```bash
# Health check
curl https://your-railway-url.up.railway.app/api/health

# Get all tracks
curl https://your-railway-url.up.railway.app/api/tracks

# Get all artists
curl https://your-railway-url.up.railway.app/api/artists

# Get all albums
curl https://your-railway-url.up.railway.app/api/albums
```

### Frontend Tests

1. Open `https://your-site.netlify.app`
2. Test:
   - ✅ Homepage loads
   - ✅ Tracks play correctly
   - ✅ Search works
   - ✅ Upload works (admin only)
   - ✅ Admin dashboard accessible
   - ✅ Mobile responsive

### Admin Tests

1. Go to `https://your-site.netlify.app/admin/`
2. Login with admin credentials
3. Test:
   - ✅ Upload new track
   - ✅ Edit track
   - ✅ Delete track
   - ✅ Add artist
   - ✅ Add album

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** Backend won't start

```bash
# Check logs in Railway dashboard
# Common issues:
# - Missing environment variables
# - Wrong PORT variable
# - Supabase credentials incorrect
```

**Problem:** CORS errors

```
Solution: Add your frontend URL to ALLOWED_ORIGINS in Railway
ALLOWED_ORIGINS=https://your-site.netlify.app
```

**Problem:** Can't upload files

```
Solution: 
1. Check Supabase storage buckets exist
2. Verify buckets are public
3. Check storage policies allow uploads
```

### Frontend Issues

**Problem:** Can't connect to API

```
Solution:
1. Check API_BASE_URL in frontend
2. Ensure backend is running
3. Check browser console for errors
```

**Problem:** Tracks won't play

```
Solution:
1. Check file URLs are accessible
2. Verify Supabase storage is public
3. Check browser console for CORS errors
```

---

## 💰 Cost Estimates

### Free Tier Limits

| Service | Free Tier | Paid Plan |
|---------|-----------|-----------|
| **Railway** | $5 credit/month | $5/month |
| **Netlify** | 100GB bandwidth/month | $19/month |
| **Supabase** | 500MB database, 1GB storage | $25/month |

**Estimated Monthly Cost:** $0 - $30 (depending on usage)

---

## 📊 Monitoring

### Railway Monitoring

- Go to **Metrics** tab in Railway
- Monitor:
  - CPU usage
  - Memory usage
  - Request count

### Netlify Analytics

- Go to **Analytics** in Netlify
- Monitor:
  - Page views
  - Bandwidth
  - Visitor locations

### Supabase Logs

- Go to **Logs** in Supabase
- Monitor:
  - Database queries
  - Storage operations

---

## 🎯 Next Steps After Deployment

1. **Set up CI/CD** - Auto-deploy on git push
2. **Add analytics** - Google Analytics, Plausible
3. **Set up error tracking** - Sentry, LogRocket
4. **Add SSL certificate** - (usually automatic)
5. **Set up backups** - Supabase auto-backups
6. **Configure CDN** - For faster global access

---

## 📞 Support

If you encounter issues:

1. Check logs in respective dashboards
2. Review error messages in browser console
3. Test API endpoints directly with curl
4. Check environment variables are correct

---

**Your DGT-SOUNDS platform is now live!** 🎉

**Share your links:**
- Frontend: `https://your-site.netlify.app`
- Admin: `https://your-site.netlify.app/admin/`
- API: `https://your-railway-url.up.railway.app`
