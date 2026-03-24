# Supabase Storage Setup Guide

## 📋 Step-by-Step Setup

### 1. Create Buckets

Go to Supabase Dashboard → **Storage**

#### Create `tracks` bucket:
1. Click **New bucket**
2. **Bucket name:** `tracks`
3. **Public bucket:** ✅ **YES** (toggle ON)
4. **File size limit:** `52428800` (50MB)
5. Click **Create bucket**

#### Create `covers` bucket:
1. Click **New bucket**
2. **Bucket name:** `covers`
3. **Public bucket:** ✅ **YES** (toggle ON)
4. **File size limit:** `5242880` (5MB)
5. Click **Create bucket**

---

## 🔐 Set Up Storage Policies (2 Options)

### Option 1: Using SQL Editor (Recommended)

1. Go to Supabase Dashboard → **SQL Editor**
2. Click **New query**
3. Copy and paste the contents of `supabase_policies.sql`
4. Click **Run** or press `Ctrl+Enter`

This will create all necessary policies for both buckets.

---

### Option 2: Using Dashboard UI

Go to **Storage** → Select bucket → **Policies** → **New policy**

#### For `tracks` bucket:

**Policy 1 - Public Read:**
- **Policy type:** Custom
- **Policy name:** `Public Read Access`
- **Allowed operation:** `SELECT`
- **Target:** `All users (public)`
- **Policy definition:**
  ```sql
  bucket_id = 'tracks'
  ```
- Click **Review** → **Save policy**

**Policy 2 - Authenticated Upload:**
- **Policy type:** Custom
- **Policy name:** `Authenticated Upload`
- **Allowed operation:** `INSERT`
- **Target:** `All users (public)` (or authenticated if you have auth)
- **Policy definition:**
  ```sql
  bucket_id = 'tracks'
  ```
- Click **Review** → **Save policy**

**Policy 3 - Authenticated Delete:**
- **Policy type:** Custom
- **Policy name:** `Authenticated Delete`
- **Allowed operation:** `DELETE`
- **Target:** `All users (public)` (or authenticated if you have auth)
- **Policy definition:**
  ```sql
  bucket_id = 'tracks'
  ```
- Click **Review** → **Save policy**

#### For `covers` bucket:

Repeat the same steps but replace `tracks` with `covers` in the policy definitions.

---

## ✅ Verify Policies

After adding policies, verify they're working:

### Test 1: Check Buckets Exist
```bash
cd backend
python test_connections.py
```

Expected output:
```
📦 Testing Supabase Storage...
   ✅ Supabase Storage: CONNECTED
      Available buckets: ['tracks', 'covers']
```

### Test 2: Try Uploading a File

Start the backend:
```bash
python main.py
```

Then go to API docs: http://localhost:8000/docs

Try the `POST /api/tracks` endpoint with:
- Title: "Test Track"
- Artist: "Test Artist"
- File: Any MP3 file
- Cover: Any JPG/PNG image (optional)

If upload succeeds → Policies are working! ✅

---

## 🔧 Troubleshooting

### Error: "permission denied for table storage.objects"

**Solution:** You need to add policies. Run the SQL from `supabase_policies.sql`

### Error: "Bucket not found"

**Solution:** Create the buckets `tracks` and `covers` in Supabase Storage

### Error: "Bucket is private"

**Solution:** Make sure buckets are set to **Public** when creating them

### Upload fails with 403 Forbidden

**Solution:** 
1. Check bucket is public
2. Verify policies allow INSERT
3. Check file size is within limits (50MB audio, 5MB images)

---

## 📊 Policy Summary

| Bucket | Public Read | Auth Upload | Auth Delete |
|--------|-------------|-------------|-------------|
| `tracks` | ✅ Yes | ✅ Yes | ✅ Yes |
| `covers` | ✅ Yes | ✅ Yes | ✅ Yes |

**Note:** The current setup allows anyone to read files (public), but only authenticated operations can upload/delete. Since we're not using Supabase Auth in this project, the backend uses the anon key which has broad permissions.

---

## 🔒 Production Security Recommendations

For production, consider:

1. **Enable Supabase Authentication** - Add user login system
2. **Restrict upload/delete** - Only allow authenticated users
3. **Add file validation** - Verify file types on server
4. **Set up CORS** - Restrict which domains can access storage
5. **Use signed URLs** - For private content access

---

## 📚 Additional Resources

- [Supabase Storage Docs](https://supabase.com/docs/guides/storage)
- [Storage Policies](https://supabase.com/docs/guides/storage/security/policies)
- [File Size Limits](https://supabase.com/docs/guides/storage/file-size-limits)

---

**Need help?** Check the main [README.md](../README.md) or [SETUP_GUIDE.md](../SETUP_GUIDE.md)
