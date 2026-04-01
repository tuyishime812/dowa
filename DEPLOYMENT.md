# 🚀 DGT-SOUNDS Deployment Guide

Complete guide to deploy your music streaming platform to production.

---

## 📋 Overview

| Component | Recommended Service | Alternative |
|-----------|-------------------|-------------|
| **Backend** | **Render** | Railway, Heroku |
| **Frontend** | **Vercel** | Netlify, Cloudflare Pages |
| **Database** | Supabase PostgreSQL | (already configured) |
| **Storage** | Supabase Storage | (already configured) |

---

## 🎯 Prerequisites

Before deploying, ensure you have:

- ✅ [GitHub account](https://github.com)
- ✅ [Supabase account](https://supabase.com) (free tier available)
- ✅ [Render account](https://render.com) (free tier available)
- ✅ [Vercel account](https://vercel.com) (free tier available)

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
ALLOWED_ORIGINS=https://your-domain.vercel.app,https://your-custom-domain.com

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

## 🔧 Step 3: Deploy Backend (Render)

### 3.1 Connect GitHub to Render

1. Go to [Render](https://render.com)
2. Click **"Login"** → **"Sign in with GitHub"**
3. Authorize Render

### 3.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Choose **"Connect a repository"**
3. Select your repository: `dowa`
4. Render will auto-detect it's a Python project

### 3.3 Configure Service

Fill in the settings:

| Setting | Value |
|---------|-------|
| **Name** | `dgt-sounds-api` (or your choice) |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### 3.4 Choose Plan

- **Free Tier**: Good for testing (spins down after inactivity)
- **Starter ($7/month)**: Always on, custom domains

### 3.5 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://your-domain.vercel.app,https://your-custom-domain.com
ADMIN_EMAIL=admin@dgt-sounds.com
ADMIN_PASSWORD=your-secure-password
```

### 3.6 Deploy

1. Click **"Create Web Service"**
2. Render will build and deploy (watch logs in **Logs** tab)
3. Once deployed, copy your **Public URL** (e.g., `https://dgt-sounds-api.onrender.com`)

### 3.7 Test Backend

```bash
curl https://your-render-url.onrender.com/api/health
```

Should return: `{"status": "healthy", "message": "DGT-SOUNDS API is running"}`

⚠️ **Note**: Free tier services spin down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds to wake up.

---

## 🎨 Step 4: Deploy Frontend (Vercel)

### 4.1 Prepare Frontend

The frontend is already configured to use `window.API_BASE_URL`.

Update `frontend/index.html` (line ~289):

```html
<script>
    // Change this to your Render backend URL
    window.API_BASE_URL = 'https://your-render-url.onrender.com';
</script>
```

Also update `frontend/admin/index.html` (line ~495) with the same URL.

### 4.2 Deploy to Vercel

#### Option A: Deploy via GitHub (Recommended)

1. Go to [Vercel](https://vercel.com)
2. Click **"Add New..."** → **"Project"**
3. Under **"Import Git Repository"**, find and select `dowa`
4. Click **"Import"**

### 4.3 Configure Project

In the project configuration:

| Setting | Value |
|---------|-------|
| **Framework Preset** | `Other` |
| **Root Directory** | `./frontend` |
| **Build Command** | `echo "No build needed"` |
| **Output Directory** | `./frontend` |

### 4.4 Add Environment Variables (Optional)

Click **"Environment Variables"** → **"Add"**:

```
API_BASE_URL=https://your-render-url.onrender.com
```

### 4.5 Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy (~30 seconds)
3. Once done, you'll get a URL like: `https://dowa-xyz.vercel.app`

#### Option B: Vercel CLI (Quick)

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to project root
cd path/to/dowa

# Deploy
vercel --prod
```

### 4.6 Update CORS on Backend

Add your Vercel URL to Render environment variables:

```
ALLOWED_ORIGINS=https://your-domain.vercel.app,https://www.your-domain.com
```

Go to Render dashboard → Your service → **Environment** → Update → Save

Redeploy will happen automatically.

---

## 🌐 Step 5: Custom Domain (Optional)
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

1. Open `https://your-site.vercel.app`
2. Test:
   - ✅ Homepage loads
   - ✅ Tracks play correctly
   - ✅ Search works
   - ✅ Upload works (admin only)
   - ✅ Admin dashboard accessible
   - ✅ Mobile responsive

### Admin Tests

1. Go to `https://your-site.vercel.app/admin/`
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
# Check logs in Render dashboard
# Common issues:
# - Missing environment variables
# - Wrong PORT variable
# - Supabase credentials incorrect
```

**Problem:** Backend slow to respond

```
Solution: Free tier spins down after 15 min inactivity
Upgrade to Starter plan ($7/mo) for always-on service
```

**Problem:** CORS errors

```
Solution: Add your Vercel URL to ALLOWED_ORIGINS in Render
ALLOWED_ORIGINS=https://your-site.vercel.app
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
| **Render** | 750 hours/month | $7/month (Starter) |
| **Vercel** | Unlimited projects | $20/month (Pro) |
| **Supabase** | 500MB database, 1GB storage | $25/month (Pro) |

**Estimated Monthly Cost:** $0 - $32 (depending on usage)

**Recommendation:** Start with free tiers, upgrade Render to Starter ($7) for production

---

## 📊 Monitoring

### Render Monitoring

- Go to **Dashboard** → Your service
- Monitor:
  - Request count
  - Response times
  - Error rates
  - CPU/Memory usage

### Vercel Analytics

- Go to **Analytics** in Vercel dashboard
- Monitor:
  - Page views
  - Web Vitals
  - Visitor locations

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
