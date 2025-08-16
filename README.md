# StudyRNA – Admin + Direct GoFile Upload (Render-ready)

## What this does
- Flask handles **admin login** only (no server-side file storage).
- The upload happens **directly from browser → GoFile** via `https://api.gofile.io/upload`.
- Works on Render, Netlify, etc. without using server storage.

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:5000

## Deploy on Render
1. Push these files to a GitHub repo.
2. Create **New Web Service** on Render and connect repo.
3. Render will use `Procfile` → `web: gunicorn app:app`
4. (Optional) Environment variables:
   - `SECRET_KEY`: your-secret
   - `ADMIN_PASSWORD`: change admin password

## Notes
- Large files (e.g., 600MB) upload directly to GoFile; your server storage is not used.
- Progress bar on the page uses XHR to show progress.
