# 🚀 CHEMIZER ANALYTICS - SETUP GUIDE

Complete manual setup instructions for Backend, Desktop App, and Web Frontend.

---

## ⚠️ IMPORTANT: DATABASE & FILES INFORMATION

### 📦 Database (db.sqlite3)
The database file is **automatically created** when you run Django migrations:
- **Location**: `backend/db.sqlite3`
- **Created by**: `python manage.py migrate` command
- **Contains**: User accounts, uploads history, authentication tokens, session data
- **First time setup**: Run migrations once, the file is generated automatically
- **Subsequent runs**: The database persists - all user data is saved

### 📁 Generated Files
These folders are **auto-created** during app usage (don't manually create them):
- `backend/uploaded_files/` - Stores uploaded CSV/Excel files
- `backend/media/` - Stores generated PDF reports
- `desktop-app/session_manager/` - Stores 48-hour session data
- `attached_assets/generated_images/` - Generated chart images

---

## 📋 INSTALLATION STEPS

### ✅ STEP 1: BACKEND SETUP

#### 1.1 Navigate to Backend Folder
```bash
cd backend
```

#### 1.2 Install Python Dependencies
```bash
pip install -r requirements.txt
```
**What this does**: Installs Django, djangorestframework, pandas, reportlab, and all other required Python packages.

#### 1.3 Create `backend/.env` File

Create a new file named `.env` in the `backend/` folder with these values:

```env
SECRET_KEY=your-django-secret-key
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
GOOGLE_OAUTH_SECRET=your-google-oauth-secret
```

**How to get these values:**

- **SECRET_KEY**: Run this command:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Copy the output and paste into `.env`

- **EMAIL_HOST_USER**: Your Gmail address (e.g., `your-email@gmail.com`)

- **EMAIL_HOST_PASSWORD**: Get from [Google Account Settings](https://support.google.com/accounts/answer/185833)
  - Enable 2-Factor Authentication first
  - Go to "App passwords"
  - Select "Mail" and "Windows Computer"
  - Copy the generated password

- **GOOGLE_OAUTH_CLIENT_ID & GOOGLE_OAUTH_SECRET**: See section "How to Get Google OAuth Credentials" at bottom of this file

#### 1.4 Create Database (db.sqlite3)

Run migrations to create the database:
```bash
python manage.py migrate
```

**What this does:**
- Creates `backend/db.sqlite3` automatically
- Sets up all database tables (users, uploads, sessions, etc.)
- File is created in your backend folder
- You only run this once on first setup

**Output you should see:**
```
Operations to perform:
  Apply all migrations: admin, auth, authtoken, accounts, ...
Running migrations:
  Applying accounts.0001_initial... OK
  Applying accounts.0002_initial... OK
  ...
```

#### 1.5 Start Backend Server

```bash
python manage.py runserver 0.0.0.0:8000
```

**Output you should see:**
```
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

✅ **Backend is now running on**: `http://localhost:8000/api`

**Keep this terminal open and running.**

---

### ✅ STEP 2: FRONTEND WEB SETUP

**Open a NEW terminal window** and follow these steps:

#### 2.1 Navigate to Web Folder
```bash
cd web
```

#### 2.2 Install Node.js Dependencies
```bash
npm install
```
**What this does**: Installs React, Vite, TypeScript, and all frontend packages.

#### 2.3 Create `web/.env` File

Create a new file named `.env` in the `web/` folder with these values:

```env
VITE_GOOGLE_CLIENT_ID=your-google-oauth-client-id
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

**How to get these values:**

- **VITE_GOOGLE_CLIENT_ID**: Same value from backend setup (from Google Cloud Console)
- **VITE_API_BASE_URL**: Should be `http://127.0.0.1:8000/api` if backend runs on port 8000

#### 2.4 Start Web Frontend

```bash
npm run dev
```

**Output you should see:**
```
VITE v4.x.x  build 0.00s
  ➜  Local:   http://localhost:5000/
  ➜  Press q + enter to quit
```

✅ **Web app is now running on**: `http://localhost:5000`

**Keep this terminal open and running.**

---

### ✅ STEP 3: DESKTOP APP SETUP

**Open a NEW terminal window** (3rd terminal) and follow these steps:

#### 3.1 Navigate to Desktop App Folder
```bash
cd desktop-app
```

#### 3.2 Install Python Dependencies
```bash
pip install -r requirements.txt
```
**What this does**: Installs PyQt5, requests, and all desktop app dependencies.

#### 3.3 Create `desktop-app/.env` File

Create a new file named `.env` in the `desktop-app/` folder with these values:

```env
API_BASE_URL=http://127.0.0.1:8000/api
GOOGLE_CLIENT_ID=your-google-oauth-client-id
DEBUG=True
```

**How to get these values:**

- **API_BASE_URL**: Should be `http://127.0.0.1:8000/api` (backend server address)
- **GOOGLE_CLIENT_ID**: Same value from backend setup

#### 3.4 Start Desktop Application

```bash
python main.py
```

**Output you should see:**
- A new window opens with "Chemizer Analytics" desktop app
- Login screen appears

✅ **Desktop app is now running**

---

## 🎯 SUMMARY: ALL 3 TERMINALS RUNNING

Now you should have **3 terminal windows** open and running:

| Terminal | Service | Command | Port | Status |
|----------|---------|---------|------|--------|
| 1 | Backend | `python manage.py runserver 0.0.0.0:8000` | 8000 | Running |
| 2 | Web App | `npm run dev` | 5000 | Running |
| 3 | Desktop | `python main.py` | N/A | Running |

**All 3 services should be running simultaneously.**

---

## 📁 ENVIRONMENT FILES SUMMARY

### `backend/.env` Example
```env
SECRET_KEY=django-insecure-abc123xyz...
EMAIL_HOST_USER=myemail@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
GOOGLE_OAUTH_CLIENT_ID=123456789.apps.googleusercontent.com
GOOGLE_OAUTH_SECRET=GOCSPX-xxxxx...
```

### `web/.env` Example
```env
VITE_GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### `desktop-app/.env` Example
```env
API_BASE_URL=http://127.0.0.1:8000/api
GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
DEBUG=True
```

---

## 🔗 CONNECTIVITY CHECK

After starting all services, verify they work:

### 1. **Web connects to Backend**
- Open browser: `http://localhost:5000`
- Try to login or signup
- Should work without errors

### 2. **Desktop connects to Backend**
- Desktop app opened from terminal 3
- Try to login
- Should work without errors

### 3. **Database working**
- Login successfully
- User should be saved in `backend/db.sqlite3`
- Try uploading a file
- Check that `backend/db.sqlite3` file exists

---

## ✨ KEY FEATURES

Your application includes:

✅ User authentication with OTP (Email-based)
✅ File upload (CSV & Excel)
✅ Data analysis with 7 chart types
✅ PDF report generation with embedded charts
✅ 48-hour session persistence
✅ Data export (CSV)
✅ Account management
✅ Responsive web interface
✅ Professional desktop application
✅ Complete REST API backend

---

## 🐛 TROUBLESHOOTING

### ❌ Backend won't start

**Error**: `ModuleNotFoundError: No module named 'django'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
```

### ❌ "Port 8000 is already in use"

**Solution:** 
- Stop any other process using port 8000
- Or use a different port:
  ```bash
  python manage.py runserver 0.0.0.0:8001
  ```

### ❌ Web app won't start

**Error**: `npm: command not found`

**Solution:** Install Node.js from https://nodejs.org/

```bash
cd web
npm install
npm run dev
```

### ❌ Desktop app can't connect to backend

**Check:**
1. Backend is running on port 8000
2. `desktop-app/.env` has correct `API_BASE_URL=http://127.0.0.1:8000/api`
3. Firewall allows localhost:8000

### ❌ Database not created

**Solution:** Run migrations:
```bash
cd backend
python manage.py migrate
```

This creates `backend/db.sqlite3` automatically.

### ❌ "No such file or directory: db.sqlite3"

**Reason**: You haven't run migrations yet

**Solution:**
```bash
cd backend
python manage.py migrate
```

### ❌ Module not found errors

**For backend:**
```bash
cd backend
pip install -r requirements.txt
```

**For web:**
```bash
cd web
npm install
```

**For desktop:**
```bash
cd desktop-app
pip install -r requirements.txt
```

### ❌ Can't find .env files

**Solution:** Create them in the correct folders:
- `backend/.env` - in the backend folder
- `web/.env` - in the web folder
- `desktop-app/.env` - in the desktop-app folder

These are required for the app to work!

---

## 📊 SERVICES OVERVIEW

| Component | Port | Technology | Startup Command | Folder |
|-----------|------|-----------|---------|--------|
| Backend API | 8000 | Django | `python manage.py runserver 0.0.0.0:8000` | `backend/` |
| Web Frontend | 5000 | React + Vite | `npm run dev` | `web/` |
| Desktop App | N/A | PyQt5 | `python main.py` | `desktop-app/` |

---

## 🔐 HOW TO GET GOOGLE OAUTH CREDENTIALS

### Step 1: Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### Step 2: Create a New Project
1. Click "Select a Project"
2. Click "New Project"
3. Name it "Chemizer Analytics"
4. Click "Create"

### Step 3: Enable Google+ API
1. Search for "Google+ API" in the search bar
2. Click "Google+ API"
3. Click "Enable"

### Step 4: Create OAuth Credentials
1. Go to "Credentials" in left menu
2. Click "Create Credentials"
3. Choose "OAuth Client ID"
4. Select "Web Application"
5. Add authorized redirect URIs:
   ```
   http://localhost:8000/accounts/google/callback/
   http://127.0.0.1:8000/accounts/google/callback/
   ```
6. Click "Create"

### Step 5: Copy Your Credentials
1. You will see "Client ID" and "Client Secret"
2. Copy these values exactly
3. Add them to your `.env` files:
   - **backend/.env**: `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_SECRET`
   - **web/.env**: `VITE_GOOGLE_CLIENT_ID`
   - **desktop-app/.env**: `GOOGLE_CLIENT_ID`

---

## 🚀 QUICK REFERENCE

### First Time Setup (Do once):
```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
# Create backend/.env file with your credentials
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# Terminal 2 - Web
cd web
npm install
# Create web/.env file with your credentials
npm run dev

# Terminal 3 - Desktop
cd desktop-app
pip install -r requirements.txt
# Create desktop-app/.env file with your credentials
python main.py
```

### Subsequent Runs (After first setup):
Just run the server commands in 3 terminals:
```
Terminal 1: cd backend && python manage.py runserver 0.0.0.0:8000
Terminal 2: cd web && npm run dev
Terminal 3: cd desktop-app && python main.py
```

---

## 📝 FILES CREATED BY THE SYSTEM

### Automatic Database Creation
- `backend/db.sqlite3` - Created by `python manage.py migrate`

### Automatic Folders Created During Use
- `backend/uploaded_files/` - User uploaded files stored here
- `backend/media/` - PDF reports stored here
- `attached_assets/generated_images/` - Chart images for PDFs

### Session Data (Desktop App)
- `~/.chemizer/session.json` - Desktop app 48-hour session storage

---

## ✅ You're ready!

1. Open 3 terminals
2. Run the startup commands in each
3. Open browser: `http://localhost:5000`
4. Start using the app!

**Made with Love for Chemical Data Analysis**
