# 🚀 Deploy DGT-SOUNDS on Vercel (Complete Guide)

Deploy both **backend** and **frontend** on Vercel as a unified application.

---

## ⚠️ Important Notes

**Vercel Serverless Limitations:**
- ⏱️ **Timeout**: 10 seconds (Hobby), 60 seconds (Pro)
- 📦 **Payload**: 4.5 MB request/response limit
- ❄️ **Cold starts**: ~1-3 seconds on first request
- 🚫 **No file uploads** > 4.5 MB
- ⚡ **Stateless**: No persistent connections

**For production with heavy uploads, consider:**
- Backend: **Render** or **Railway** (always-on servers)
- Frontend: **Vercel** (perfect for static sites)

---

## 📋 Prerequisites

- ✅ [Vercel account](https://vercel.com) (free tier available)
- ✅ [Supabase project](https://supabase.com) set up
- ✅ GitHub repository pushed

---

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Files already created for you:
- ✅ `api/index.py` - Vercel serverless entry point
- ✅ `vercel.json` - Vercel configuration
- ✅ Frontend configured for Vercel

### Step 2: Install Vercel CLI (Optional but Recommended)

```bash
npm install -g vercel
```

### Step 3: Deploy via Vercel Dashboard (Easiest)

#### 3.1 Connect GitHub to Vercel

1. Go to [Vercel](https://vercel.com)
2. Click **"Add New..."** → **"Project"**
3. Click **"Import Git Repository"**
4. Find and select `dowa` repository
5. Click **"Import"**

#### 3.2 Configure Project

**Project Settings:**

| Setting | Value |
|---------|-------|
| **Framework Preset** | `Other` |
| **Root Directory** | `./` (keep default) |
| **Build Command** | `echo "No build needed"` |
| **Output Directory** | `frontend` |
| **Install Command** | `pip install -r backend/requirements.txt` |

#### 3.3 Add Environment Variables

Click **"Environment Variables"** → Add each:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
ADMIN_EMAIL=admin@dgt-sounds.com
ADMIN_PASSWORD=admin123
ALLOWED_ORIGINS=https://dowa-*.vercel.app
```

⚠️ **Important**: Replace with your actual Supabase credentials!

#### 3.4 Deploy

1. Click **"Deploy"**
2. Wait for build (~2-3 minutes)
3. Once complete, you'll get a URL: `https://dowa-xyz.vercel.app`

---

### Step 4: Deploy via Vercel CLI (Alternative)

```bash
# Login to Vercel
vercel login

# Navigate to project
cd C:\Users\Student.LAPTOP-46MOQA5A\Desktop\projects\dowa

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

---

## 🔧 Step 5: Update Frontend API URL

Update `frontend/index.html` (line ~289):

```html
<script>
    // For Vercel deployment, use relative URL
    window.API_BASE_URL = '';  // Empty = use same domain
    // Or specify your Vercel URL:
    // window.API_BASE_URL = 'https://your-domain.vercel.app';
</script>
```

Update `frontend/admin/index.html` (line ~495) similarly.

---

## 🧪 Step 6: Test Your Deployment

### Test Frontend

1. Open `https://your-domain.vercel.app`
2. Check:
   - ✅ Homepage loads
   - ✅ Tracks play
   - ✅ Search works
   - ✅ No console errors

### Test Backend API

```bash
# Replace with your Vercel URL
curl https://your-domain.vercel.app/api/health
curl https://your-domain.vercel.app/api/tracks
curl https://your-domain.vercel.app/api/artists
curl https://your-domain.vercel.app/api/albums
```

Expected response:
```json
{"status": "healthy", "message": "DGT-SOUNDS API is running"}
```

### Test Admin Dashboard

1. Go to `https://your-domain.vercel.app/admin/`
2. Login: `admin@dgt-sounds.com` / `admin123`
3. Test:
   - ✅ Dashboard loads
   - ✅ Upload track works
   - ✅ CRUD operations work

---

## ⚡ Performance Optimization

### 1. Enable Vercel Caching

Add to `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### 2. Optimize Supabase Queries

- Use indexes (already configured)
- Limit result sets
- Enable connection pooling

### 3. Reduce Cold Starts

- Upgrade to Vercel Pro ($20/month) for faster cold starts
- Use `regions` in `vercel.json` to deploy closer to users
- Keep dependencies minimal

---

## 🚨 Troubleshooting

### Issue: API Timeout

**Problem**: Request takes > 10 seconds

**Solutions**:
1. Upgrade to Vercel Pro (60s timeout)
2. Optimize database queries
3. Move backend to Render/Railway

### Issue: File Upload Fails

**Problem**: Upload fails for large files

**Solutions**:
1. Reduce file size limit
2. Upload directly to Supabase Storage (bypass API)
3. Use presigned URLs for direct upload

### Issue: CORS Errors

**Problem**: Frontend can't connect to API

**Solution**:
```env
ALLOWED_ORIGINS=https://your-domain.vercel.app
```

Add to Vercel Environment Variables.

### Issue: Cold Start Delay

**Problem**: First request is slow (~3 seconds)

**Solutions**:
1. Upgrade to Vercel Pro
2. Use uptime monitoring to keep warm
3. Move backend to Render (always-on)

### Issue: Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'backend'`

**Solution**:
Check `api/index.py` path is correct:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
```

---

## 💰 Cost Comparison

| Service | Free Tier | Pro Tier |
|---------|-----------|----------|
| **Vercel** | Unlimited projects, 100GB bandwidth | $20/month |
| **Supabase** | 500MB DB, 1GB storage | $25/month |

**Total**: $0 - $45/month

---

## 🎯 Recommended Architecture

### For Testing/Hobby:
```
Frontend + Backend → Vercel (Free)
Database + Storage → Supabase (Free)
```

### For Production:
```
Frontend → Vercel Pro ($20)
Backend → Render Starter ($7)
Database + Storage → Supabase Pro ($25)
Total: $52/month
```

---

## 📊 Monitoring

### Vercel Dashboard

- **Analytics**: Page views, performance
- **Logs**: Function logs, errors
- **Metrics**: Response times, errors

### Supabase Dashboard

- **Logs**: Database queries
- **Storage**: File uploads, bandwidth

---

## 🔐 Security Checklist

- [ ] Change default admin password
- [ ] Enable Supabase RLS (Row Level Security)
- [ ] Set proper CORS origins
- [ ] Use environment variables (never commit `.env`)
- [ ] Enable HTTPS (automatic on Vercel)
- [ ] Rate limit API endpoints

---

## ✅ Deployment Checklist

Before going live:

- [ ] Supabase database schema applied
- [ ] Storage buckets created (`tracks`, `covers`)
- [ ] Environment variables set in Vercel
- [ ] Frontend API URL configured
- [ ] Test all CRUD operations
- [ ] Test file uploads
- [ ] Test audio playback
- [ ] Check mobile responsiveness
- [ ] Update admin password
- [ ] Set up custom domain (optional)

---

## 🌐 Custom Domain (Optional)

### On Vercel:

1. Go to **Project Settings** → **Domains**
2. Add your domain: `dgt-sounds.com`
3. Update DNS records:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   ```
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```

---

## 🎉 Success!

Your DGT-SOUNDS platform is now live on Vercel!

**Your URLs:**
- 🎵 Frontend: `https://your-domain.vercel.app`
- 🔧 Admin: `https://your-domain.vercel.app/admin/`
- ⚡ API: `https://your-domain.vercel.app/api/`

---

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
