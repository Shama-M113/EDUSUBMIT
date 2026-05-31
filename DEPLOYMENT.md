# Deployment Guide - EduSubmit

## **Quick Start: Deploy to Render**

### **Step 1: Prepare Your Repository**

1. **Commit all changes to Git:**
```bash
cd "c:\Users\SHAMA\Desktop\EDU UPDATED - Copy (2)"
git add .
git commit -m "Prepare for production deployment"
```

2. **Push to GitHub** (if not already done):
```bash
git remote add origin https://github.com/YOUR_USERNAME/edusubmit.git
git branch -M main
git push -u origin main
```

---

### **Step 2: Create Render Account & Deploy**

1. **Go to [render.com](https://render.com)** and sign up for free
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository:**
   - Click "Connect Repository"
   - Search for your repo
   - Click "Connect"

4. **Configure settings:**
   - **Name:** edusubmit
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free tier (for testing)

5. **Add Environment Variables:**
   - Click "Advanced"
   - Add new environment variable:
     - **Key:** `SECRET_KEY`
     - **Value:** Generate a strong key: https://randomkeygen.com/
   - Click "Create Web Service"

**Render will automatically deploy your app!** 🚀

---

### **Step 3: Database Setup (Important!)**

Since your database is SQLite (file-based), it will **reset every time Render redeploys**. For production, upgrade to PostgreSQL:

**Option A: Use Render PostgreSQL** (Recommended)
```
1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Name: edusubmit-db
4. Use free plan
5. Copy the connection URL
6. In Web Service, add env var: DATABASE_URL = <connection_url>
```

**Then update your Python code:**
```python
import psycopg2
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
# Use this for PostgreSQL connections instead of SQLite
```

**Option B: Keep SQLite** (Not recommended for production)
- Data resets on every deploy
- Only use for testing/demo

---

### **Step 4: Initialize Database**

1. **SSH into Render:** Click your service → Shell
2. **Run initialization scripts:**
```bash
python load_student.py
python load_teachers.py
python load_assignments.py
python load_submissions.py
```

---

### **Step 5: Get Your Live URL**

Your app is now live at:
```
https://edusubmit.onrender.com
```

---

## **Important: Security Checklist**

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Don't commit `database.db` to git (.gitignore already added)
- [ ] Use HTTPS (Render provides this automatically)
- [ ] Change default admin passwords
- [ ] Add environment variables for all secrets

---

## **Troubleshooting**

**App won't start?**
- Check logs: Render Dashboard → Logs
- Look for missing dependencies
- Verify Procfile is correct

**Database errors?**
- Use PostgreSQL instead of SQLite
- Check database migrations ran

**Files disappearing?**
- SQLite files reset on deploy
- Migrate to PostgreSQL or add file uploads to database

---

## **Costs**

- **Free Plan:** $0 (sleeps after 15 mins of inactivity)
- **Standard:** $7/month (always on)

---

## **Manual Deployment Steps Summary**

1. ✅ Update app.py (debug=False, use PORT env var)
2. ✅ Create requirements.txt with all dependencies
3. ✅ Create Procfile for Gunicorn
4. ✅ Create render.yaml for Render config
5. ✅ Add .gitignore
6. ✅ Push to GitHub
7. ✅ Connect GitHub to Render
8. ✅ Set environment variables
9. ✅ Initialize database
10. ✅ Test your live app!

