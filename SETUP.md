# 🚀 CHEMIZER ANALYTICS - SETUP GUIDE

Complete setup instructions for Backend, Desktop App, and Web Frontend.

---

## 📋 INSTALLATION STEPS

### STEP 1: BACKEND SETUP

#### 1.1 Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 1.2 Create `backend/.env` File

Create a new file named `.env` in the `backend/` folder and add these values:

```env
SECRET_KEY=your-django-secret-key
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
GOOGLE_OAUTH_SECRET=your-google-oauth-secret
```

**How to get these values:**

- **SECRET_KEY**: Found in `backend/settings.py` - use a secure random string or generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- **EMAIL_HOST_USER**: Your Gmail address (for sending OTP emails)
- **EMAIL_HOST_PASSWORD**: Gmail app password from [Google Account Settings](https://support.google.com/accounts/answer/185833)
- **GOOGLE_OAUTH_CLIENT_ID & GOOGLE_OAUTH_SECRET**: From [Google Cloud Console](https://console.cloud.google.com/) - see section "How to Get Google OAuth Credentials" below

#### 1.3 Apply Database Migrations
```bash
cd backend
python manage.py migrate
```

#### 1.4 Start Backend Server
```bash
./run-backend.sh
```

Backend is now running on: **http://localhost:8000/api**

---

### STEP 2: DESKTOP APP SETUP

#### 2.1 Install Desktop Dependencies
```bash
cd desktop-app
pip install -r requirements.txt
```

#### 2.2 Create `desktop-app/.env` File

Create a new file named `.env` in the `desktop-app/` folder and add these values:

```env
API_BASE_URL=http://127.0.0.1:8000/api
GOOGLE_CLIENT_ID=your-google-oauth-client-id
DEBUG=True
```

**How to get these values:**

- **API_BASE_URL**: Your backend API address (usually `http://127.0.0.1:8000/api` if running locally)
- **GOOGLE_CLIENT_ID**: Same as backend setup (from Google Cloud Console)

#### 2.3 Make Sure Backend is Running

In another terminal, ensure the backend is running:
```bash
./run-backend.sh
```

#### 2.4 Start Desktop App
```bash
./run-desktop.sh
```

Desktop app will launch and connect to the backend.

---

### STEP 3: WEB FRONTEND SETUP

#### 3.1 Install Web Dependencies
```bash
cd web
npm install
```

#### 3.2 Create `web/.env` File

Create a new file named `.env` in the `web/` folder and add these values:

```env
VITE_GOOGLE_CLIENT_ID=your-google-oauth-client-id
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

**How to get these values:**

- **VITE_GOOGLE_CLIENT_ID**: Same as backend setup (from Google Cloud Console)
- **VITE_API_BASE_URL**: Your backend API address (usually `http://127.0.0.1:8000/api` if running locally)

#### 3.3 Make Sure Backend is Running

In another terminal, ensure the backend is running:
```bash
./run-backend.sh
```

#### 3.4 Start Web Frontend
```bash
./run-web.sh
```

Web app will start on: **http://localhost:5000**

---

## 🚀 RUNNING THE APPLICATION

### RECOMMENDED: Run Everything at Once

From root folder:
```bash
./run-all.sh
```

This will start:
- Backend on port 8000
- Web app on port 5000
- Desktop app (separate window)

### Manual Startup (3 separate terminals)

**Terminal 1 - Backend:**
```bash
./run-backend.sh
```

**Terminal 2 - Web:**
```bash
./run-web.sh
```

**Terminal 3 - Desktop:**
```bash
./run-desktop.sh
```

---

## 📁 ENVIRONMENT FILES SUMMARY

### `backend/.env`
```env
SECRET_KEY=secret-key-from-settings-py
EMAIL_HOST_USER=gmail-address
EMAIL_HOST_PASSWORD=gmail-app-password
GOOGLE_OAUTH_CLIENT_ID=google-client-id
GOOGLE_OAUTH_SECRET=google-oauth-secret
```

### `web/.env`
```env
VITE_GOOGLE_CLIENT_ID=google-client-id
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### `desktop-app/.env`
```env
API_BASE_URL=http://127.0.0.1:8000/api
GOOGLE_CLIENT_ID=google-client-id
DEBUG=True
```

---

## 🔗 CONNECTIVITY CHECK

After starting all services, verify they are connected:

1. **Web connects to Backend:**
   - Open http://localhost:5000
   - Try login/signup
   - Should work without errors

2. **Desktop connects to Backend:**
   - Launch desktop app
   - Try login
   - Should work without errors

3. **Web can upload files:**
   - Upload a CSV/Excel file
   - Should process and show results

---

## ✨ FEATURES

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

### Backend won't start?
Follow these steps:
1. Go to backend folder: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver 0.0.0.0:8000`

### Can't connect to backend?
Follow these steps:
1. Check if backend is running on port 8000
2. Verify `.env` files have correct `API_BASE_URL`
3. Make sure firewall allows localhost:8000
4. Check backend terminal for error messages

### Module not found errors?
Follow these steps:
1. For backend: `cd backend && pip install -r requirements.txt`
2. For web: `cd web && npm install`
3. For desktop: `cd desktop-app && pip install -r requirements.txt`

### Port already in use?
Follow these steps:
1. Identify which process is using the port
2. Stop that process and try again
3. Or use different ports in the run scripts

---

## 📊 SERVICES OVERVIEW

| Service | Port | Technology | Command |
|---------|------|-----------|---------|
| Backend | 8000 | Django | `./run-backend.sh` |
| Web App | 5000 | React + Vite | `./run-web.sh` |
| Desktop | N/A | PyQt5 | `./run-desktop.sh` |

---

## 🔐 HOW TO GET GOOGLE OAUTH CREDENTIALS

### Step 1: Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### Step 2: Create a New Project
1. Click "Select a Project"
2. Click "New Project"
3. Name it "Chemizer Analytics"
4. Click "Create"

### Step 3: Enable Google OAuth API
1. Search for "Google+ API"
2. Click "Enable"

### Step 4: Create OAuth Credentials
1. Go to "Credentials" in left menu
2. Click "Create Credentials"
3. Choose "OAuth Client ID"
4. Select "Web Application"
5. Add authorized redirect URIs:
   - http://localhost:8000/accounts/google/callback/
   - http://127.0.0.1:8000/accounts/google/callback/
6. Click "Create"

### Step 5: Copy Your Credentials
1. You will see "Client ID" and "Client Secret"
2. Copy these values
3. Add them to your `.env` files:
   - **backend/.env**: GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_SECRET
   - **web/.env**: VITE_GOOGLE_CLIENT_ID
   - **desktop-app/.env**: GOOGLE_CLIENT_ID

---

**✅ You're ready! Start with: `./run-all.sh`**

Essential files:
- `backend/` - All Django backend code
- `web/` - All React frontend code
- `package.json` / `requirements.txt` - Dependencies
- `.env` files - Your credentials
- `node_modules/` - Auto-generated, don't delete
- `.pythonlibs/` - Auto-generated, don't delete

---

## Troubleshooting

**"Module not found" errors:**
```bash
cd web && npm install
cd backend && pip install -r requirements.txt
```

**"Port already in use":**
```bash
# Kill processes on ports 5000 or 8000
killall -9 node python
```

**Google OAuth not working:**
- Check `.env` files have correct client ID
- Make sure no extra spaces in credentials
- Verify redirect URIs in Google Console

---

That's it! 🚀
