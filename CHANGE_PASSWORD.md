# How to Change Admin Password

## Method 1: Render Dashboard (Easiest)

1. Go to https://dashboard.render.com
2. Click on `dgt-sounds-api`
3. Go to **Environment** tab
4. Update these variables:
   - `ADMIN_EMAIL` = your-new-email@example.com
   - `ADMIN_PASSWORD` = your-new-secure-password
5. Click **Save Changes**
6. Wait for redeploy (~1 minute)

## Method 2: Using API (Advanced)

You can also change password via API call:

```bash
curl -X PUT https://dgt-sounds-api.onrender.com/api/admin/settings/password \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"newPassword": "your-new-password"}'
```

## Security Recommendations

✅ **Strong Password Requirements:**
- At least 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- No common words or patterns

✅ **Email:**
- Use a real email you own
- Not the same as your personal email

✅ **Store Securely:**
- Save credentials in a password manager
- Don't share publicly

## Current Default Credentials

```
Email: admin@dgt-sounds.com
Password: admin123
```

⚠️ **Change these immediately for production!**
