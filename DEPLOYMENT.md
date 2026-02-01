# Deployment Guide - Render

## Quick Start

### 1. Connect GitHub to Render
- Go to [render.com](https://render.com)
- Sign up / Log in
- Click **+ New** → **Web Service**
- Connect your GitHub account and select this repository

### 2. Configure Web Service
- **Name:** `mental-health-platform`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Instance Type:** Free (or Starter for production)

### 3. Add Environment Variables
In Render dashboard → Service Settings → **Environment**:

```
SECRET_KEY=<generate-with-python-secrets-token-hex-32>
FLASK_ENV=production
```

Generate secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Deploy
- Click **Create Web Service**
- Render will automatically:
  - Clone your repo
  - Install dependencies
  - Start the app
  - Assign a live URL

### 5. Initialize Database
After deployment, use Render's Shell feature:
```bash
python init_db.py
```

Or manually navigate to the app and register users.

---

## Production Checklist

✅ `requirements.txt` updated with gunicorn  
✅ `Procfile` configured  
✅ `runtime.txt` specifies Python 3.10.11  
✅ `SECRET_KEY` set in environment  
✅ Database SQLite ready (or upgrade to PostgreSQL)  
✅ GitHub repo committed and pushed  

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Check logs; ensure all imports in `app.py` have dependencies in `requirements.txt` |
| 502 Bad Gateway | App crashed; check Render logs for errors |
| Database empty | Run `init_db.py` in Render Shell or re-deploy |
| Static files missing | Ensure `static/` folder is in repo |

---

## Database Migration (Optional)

For production, upgrade to PostgreSQL:

1. Create PostgreSQL instance in Render
2. Copy connection URL
3. Add `DATABASE_URL` environment variable to Web Service
4. Re-deploy

Your app will auto-detect PostgreSQL and use it.

---

## Next Steps

1. Commit all changes:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push
   ```

2. Go to [render.com](https://render.com)
3. Follow the Web Service setup above
4. Share your live URL when deployed!
