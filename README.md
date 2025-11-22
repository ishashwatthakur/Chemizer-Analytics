# 🧪 CHEMIZER ANALYTICS

**Professional Chemical Equipment Data Analysis Platform**

A comprehensive web and desktop application for analyzing chemical equipment data from CSV/Excel files, generating detailed reports with visualizations, and managing analyzed data through a secure authentication system.

---

## 📋 TABLE OF CONTENTS

- [About](#about)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [File Descriptions](#file-descriptions)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [Architecture Overview](#architecture-overview)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)

---

## 🎯 ABOUT

**Chemizer Analytics** is a full-stack application designed for chemical data analysis. It provides:

- **Web Platform**: React + Vite frontend with responsive design for desktop and tablet users
- **Desktop Application**: PyQt5 native application for Windows/Linux/Mac with 48-hour session persistence
- **Backend API**: Django REST Framework with secure authentication and file processing
- **Analysis Engine**: Advanced data analysis with multiple chart types and PDF report generation

The application allows users to:
1. Upload chemical equipment data (CSV or Excel files)
2. Analyze the data with interactive visualizations
3. Export results as CSV files or PDF reports
4. Manage their account and data securely
5. Access their data across web and desktop applications

---

## ✨ FEATURES

### 🔐 Authentication & Security
- **Email-based OTP (One-Time Password)** - Secure login without passwords
- **Google OAuth 2.0** - Single sign-on for web users
- **48-hour Session Persistence** - Stay logged in for 48 hours (web and desktop)
- **Account Management** - User profiles, password management, data deletion
- **Secure API** - Token-based authentication for all endpoints

### 📊 Data Analysis
- **File Upload Support** - CSV and Excel (.xlsx, .xls) file formats
- **7 Chart Types** - Line, Bar, Area, Scatter, Pie, Histogram, Box Plot
- **Statistical Analysis** - Mean, Median, Standard Deviation, Min, Max calculations
- **Data Export** - Export analyzed data as CSV files
- **Heatmap & Correlation Matrix** - For numeric data analysis
- **Data Preview** - View first 100 rows with "Load More" functionality

### 📄 Report Generation
- **PDF Reports** - Professional PDF generation with all charts embedded
- **Chart Export** - All visualization types converted to images in PDF
- **Summary Statistics** - Statistical insights automatically calculated
- **Bulk Export** - Download all reports at once

### 💼 Bulk Operations
- **Multi-file Selection** - Select multiple uploaded files
- **Bulk Download** - Download multiple files in one operation
- **Bulk Delete** - Remove multiple files simultaneously
- **Batch Processing** - Process multiple files efficiently

### 🎨 User Interface
- **Responsive Design** - Works on desktop, tablet, mobile
- **Professional Theme** - Clean, modern interface with consistent design
- **Dark/Light Mode** - Theme switching capability
- **Intuitive Navigation** - Easy-to-use dashboard and workflows
- **Real-time Updates** - Instant feedback on operations

---

## 🛠️ TECHNOLOGY STACK

### **Backend**
| Technology | Purpose | Usage |
|------------|---------|-------|
| **Django** | Web framework | Core backend server, handles HTTP requests |
| **Django REST Framework** | API building | RESTful API endpoints for all operations |
| **Django-CORS** | Cross-Origin | Enable requests from web/desktop frontends |
| **django-allauth** | Authentication | User registration, email verification, OAuth |
| **PyJWT** | Token auth | JSON Web Token generation and validation |
| **pandas** | Data processing | CSV/Excel file parsing and analysis |
| **ReportLab** | PDF generation | Creating PDF reports with embedded charts |
| **SQLite/PostgreSQL** | Database | User data, file metadata, session storage |
| **python-dotenv** | Configuration | Environment variable management |

### **Web Frontend**
| Technology | Purpose | Usage |
|------------|---------|-------|
| **React 18** | UI library | Component-based user interface |
| **Vite** | Build tool | Lightning-fast development and production build |
| **TypeScript** | Language | Type-safe JavaScript development |
| **Tailwind CSS** | Styling | Utility-first CSS framework |
| **Radix UI** | Components | Accessible UI component library |
| **React Router** | Navigation | Multi-page routing (Login, Dashboard, Results, Profile) |
| **React Query** | Data fetching | Server state management and caching |
| **Recharts** | Charts | Interactive chart visualization library |
| **React Hook Form** | Forms | Efficient form management and validation |
| **Sonner** | Notifications | Toast notifications for user feedback |

### **Desktop Application**
| Technology | Purpose | Usage |
|------------|---------|-------|
| **PyQt5** | UI Framework | Native desktop interface for Windows/Linux/Mac |
| **QSS Styling** | Theming | CSS-like styling for PyQt5 components |
| **requests** | HTTP Client | API communication with backend |
| **python-dotenv** | Configuration | Environment variable management |
| **json** | Session Storage | Persistent session data storage |

### **Development & DevOps**
| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **npm** | Node package manager |
| **pip** | Python package manager |
| **Shell Scripts** | Automation (run-*.sh files) |

---

## 📁 PROJECT STRUCTURE

```
chemizer-analytics/
│
├── README.md                    # Project documentation
├── SETUP.md                     # Setup instructions (COMPLETE GUIDE)
├── CLEANUP_REPORT.txt          # Cleanup documentation
│
├── run-all.sh                  # Start all services at once
├── run-backend.sh              # Start Django backend only
├── run-web.sh                  # Start React frontend only
├── run-desktop.sh              # Start PyQt5 desktop app only
│
├── backend/                    # Django Backend
│   ├── manage.py              # Django management command
│   ├── settings.py            # Django configuration
│   ├── requirements.txt        # Python dependencies
│   ├── db.sqlite3             # SQLite database (auto-created)
│   ├── .env                   # Environment variables (create this)
│   │
│   └── accounts/              # Accounts app
│       ├── models.py          # User model and database schema
│       ├── views.py           # API endpoints (login, signup, upload, etc.)
│       ├── urls.py            # URL routing
│       ├── serializers.py     # API request/response serialization
│       └── admin.py           # Django admin interface
│
├── web/                        # React + Vite Frontend
│   ├── src/
│   │   ├── main.tsx          # React entry point
│   │   ├── App.tsx           # Main component
│   │   ├── index.css         # Global styles
│   │   │
│   │   ├── pages/            # Page components
│   │   │   ├── Dashboard.tsx # Main dashboard with upload cards
│   │   │   ├── Results.tsx   # Analysis results with charts
│   │   │   ├── Profile.tsx   # User profile management
│   │   │   └── Login.tsx     # Authentication page
│   │   │
│   │   ├── components/       # Reusable UI components
│   │   │   ├── Chart*.tsx   # Chart components
│   │   │   ├── UploadCard.tsx # Upload file card
│   │   │   ├── Button.tsx    # Custom button
│   │   │   └── ...
│   │   │
│   │   ├── contexts/         # React context
│   │   │   └── AuthContext.tsx # Authentication state
│   │   │
│   │   ├── hooks/            # Custom React hooks
│   │   │   ├── useAuth.ts   # Authentication hook
│   │   │   └── useApi.ts    # API calls hook
│   │   │
│   │   ├── lib/              # Utilities
│   │   │   ├── api.ts       # API client
│   │   │   ├── constants.ts  # Constants and config
│   │   │   └── utils.ts     # Helper functions
│   │   │
│   │   └── styles/           # Component styles (CSS modules)
│   │
│   ├── public/               # Static assets
│   ├── package.json          # Node dependencies and scripts
│   ├── vite.config.ts        # Vite build configuration
│   ├── tsconfig.json         # TypeScript configuration
│   ├── .env                  # Environment variables (create this)
│   └── tailwind.config.js    # Tailwind CSS configuration
│
├── desktop-app/              # PyQt5 Desktop Application
│   ├── main.py              # Application entry point
│   ├── api_client.py        # Backend API client
│   ├── session_manager.py   # 48-hour session persistence
│   ├── constants.py         # Design system and constants
│   ├── requirements.txt      # Python dependencies
│   ├── .env                 # Environment variables (create this)
│   │
│   ├── ui/                  # UI windows and components
│   │   ├── app_controller.py     # Main application controller
│   │   ├── login_window_new.py   # Login screen
│   │   ├── signup_window_new.py  # Registration screen
│   │   ├── main_window_new.py    # File upload window
│   │   ├── dashboard_window_new.py # Dashboard with files
│   │   ├── results_window_new.py # Analysis results
│   │   ├── profile_window_new.py # User profile
│   │   ├── otp_dialog_new.py    # OTP verification dialog
│   │   ├── navigation.py        # Navigation bar
│   │   └── styles.py           # QSS stylesheet definitions
│   │
│   └── __init__.py          # Package initialization
│
└── attached_assets/          # Generated assets and images
    └── generated_images/     # Chart images for PDF
```

---

## 📄 FILE DESCRIPTIONS

### **BACKEND FILES**

#### `backend/manage.py`
- **Purpose**: Django project management command
- **Usage**: Run migrations, start server, create superuser
- **Example**: `python manage.py runserver`

#### `backend/settings.py`
- **Purpose**: Django configuration
- **Contains**: 
  - Database settings (SQLite/PostgreSQL)
  - Installed apps and middleware
  - REST framework configuration
  - CORS settings for web/desktop apps
  - Email configuration for OTP
  - Static files configuration

#### `backend/accounts/models.py`
- **Purpose**: Database schema definition
- **Defines**: User model with email, profile data, upload history
- **Relations**: User → Upload files relationship

#### `backend/accounts/views.py`
- **Purpose**: API endpoints implementation
- **Endpoints** (15+):
  - `POST /auth/register` - User registration with OTP
  - `POST /auth/verify-otp` - Email OTP verification
  - `POST /auth/login` - Login with credentials
  - `POST /upload` - File upload and analysis
  - `GET /results/<id>` - Get analysis results
  - `GET /files` - List user's uploaded files
  - `DELETE /files/<id>` - Delete uploaded file
  - `GET /profile` - Get user profile
  - `PUT /profile` - Update profile
  - `DELETE /account` - Delete user account
  - `POST /export` - Export data as CSV/PDF
  - And more...

#### `backend/accounts/serializers.py`
- **Purpose**: Convert between Python objects and JSON
- **Serializers**: User, Upload, Results, Profile serializers

#### `backend/accounts/urls.py`
- **Purpose**: URL routing configuration
- **Maps**: URL patterns to view functions

#### `backend/requirements.txt`
- **Purpose**: Python package dependencies
- **Contains**: Django, DRF, pandas, ReportLab, etc.

#### `backend/.env`
- **Purpose**: Environment configuration
- **Variables**:
  - `SECRET_KEY` - Django secret key
  - `EMAIL_HOST_USER` - Gmail for sending OTP
  - `EMAIL_HOST_PASSWORD` - Gmail app password
  - `GOOGLE_OAUTH_CLIENT_ID` - Google OAuth ID
  - `GOOGLE_OAUTH_SECRET` - Google OAuth secret

---

### **WEB FRONTEND FILES**

#### `web/src/main.tsx`
- **Purpose**: React application entry point
- **Usage**: Mounts React app to DOM

#### `web/src/App.tsx`
- **Purpose**: Main app component
- **Contains**: Routing, authentication wrapper, layout

#### `web/src/pages/Dashboard.tsx`
- **Purpose**: Main dashboard page
- **Features**: Upload area, file list, 3-dot menus for actions
- **Data source**: Fetches user's uploaded files from backend

#### `web/src/pages/Results.tsx`
- **Purpose**: Analysis results display
- **Features**: Charts, data table, PDF download, statistics
- **Data source**: Gets results from backend analysis

#### `web/src/pages/Profile.tsx`
- **Purpose**: User profile management
- **Features**: Username/email display, password change, account deletion
- **Data source**: Fetches user profile from backend

#### `web/src/pages/Login.tsx`
- **Purpose**: Authentication page
- **Features**: Email/OTP login, Google OAuth, signup link
- **Actions**: Validates credentials, stores auth token

#### `web/src/components/`
- **ChartRenderer.tsx** - Renders all 7 chart types dynamically
- **DataTable.tsx** - Displays data preview with pagination
- **UploadCard.tsx** - File upload input with drag-drop
- **Button.tsx**, **Input.tsx** - Custom UI components
- Radix UI wrapper components

#### `web/src/contexts/AuthContext.tsx`
- **Purpose**: Global authentication state
- **Provides**: User data, login, logout, token management
- **Usage**: Wrapped around entire app

#### `web/src/hooks/useAuth.ts`
- **Purpose**: Custom hook for authentication
- **Usage**: `const { user, login, logout } = useAuth()`

#### `web/src/hooks/useApi.ts`
- **Purpose**: Custom hook for API calls
- **Usage**: Handles loading states, errors, retries

#### `web/src/lib/api.ts`
- **Purpose**: Backend API client
- **Methods**: GET, POST, PUT, DELETE requests
- **Authentication**: Adds auth token to all requests

#### `web/src/lib/constants.ts`
- **Purpose**: Application constants
- **Contains**: Colors, chart types, API endpoints, validation rules

#### `web/package.json`
- **Purpose**: Node.js project configuration
- **Contains**: Dependencies, scripts (dev, build, preview)

#### `web/vite.config.ts`
- **Purpose**: Vite build configuration
- **Configures**: Development server, build output, aliases

#### `web/.env`
- **Purpose**: Environment configuration
- **Variables**:
  - `VITE_GOOGLE_CLIENT_ID` - Google OAuth Client ID
  - `VITE_API_BASE_URL` - Backend API URL (localhost:8000)

---

### **DESKTOP APPLICATION FILES**

#### `desktop-app/main.py`
- **Purpose**: Application entry point
- **Usage**: Launches PyQt5 application
- **Creates**: Main window, initializes session manager

#### `desktop-app/api_client.py`
- **Purpose**: Backend API communication
- **Methods**: All 15+ API endpoints wrapped for desktop use
- **Features**: Request handling, error management, response parsing
- **Usage**: Called by all UI windows

#### `desktop-app/session_manager.py`
- **Purpose**: 48-hour session persistence
- **Storage**: `~/.chemizer/session.json` file
- **Features**: 
  - Automatic login on app restart
  - Session timeout after 48 hours
  - Secure token storage
  - Auto-logout handling

#### `desktop-app/constants.py`
- **Purpose**: Design system constants
- **Contains**: 
  - Colors (#2563eb, #059669, #7c3aed, #dc2626)
  - Fonts and sizes
  - API endpoints
  - UI dimensions

#### `desktop-app/ui/app_controller.py`
- **Purpose**: Main application controller
- **Manages**: Window switching, state management, API calls
- **Orchestrates**: Navigation between all windows

#### `desktop-app/ui/login_window_new.py`
- **Purpose**: Login screen interface
- **Features**: Email/OTP input, Google OAuth (future), error display
- **Signals**: Emits success signal to controller

#### `desktop-app/ui/signup_window_new.py`
- **Purpose**: User registration interface
- **Features**: Email input, password validation, terms acceptance
- **Signals**: Emits signup success signal

#### `desktop-app/ui/main_window_new.py`
- **Purpose**: File upload interface
- **Features**: Drag-drop upload, file picker, progress bar
- **Actions**: Uploads file, shows progress, navigates to results

#### `desktop-app/ui/dashboard_window_new.py`
- **Purpose**: Dashboard with file history
- **Features**: 
  - Lists all user's uploaded files
  - 3-dot menu with View/Download/Delete/Share
  - Bulk selection and operations
  - Real-time file status

#### `desktop-app/ui/results_window_new.py`
- **Purpose**: Analysis results display
- **Features**: All 7 chart types, data table, PDF download
- **Uses**: ChartRenderer for chart creation

#### `desktop-app/ui/profile_window_new.py`
- **Purpose**: User profile management
- **Features**: View profile, change password, delete account
- **Actions**: API calls to backend profile endpoints

#### `desktop-app/ui/otp_dialog_new.py`
- **Purpose**: OTP verification dialog
- **Features**: OTP input field, timer, resend button
- **Modal**: Blocks main window during verification

#### `desktop-app/ui/navigation.py`
- **Purpose**: Navigation bar component
- **Features**: Menu items, user info display, logout button
- **Layout**: Horizontal top navigation bar

#### `desktop-app/ui/styles.py`
- **Purpose**: QSS stylesheet definitions
- **Contains**: All colors, fonts, button styles, theme settings
- **Usage**: Applied to all widgets for consistent look

#### `desktop-app/.env`
- **Purpose**: Environment configuration
- **Variables**:
  - `API_BASE_URL` - Backend API URL (localhost:8000)
  - `GOOGLE_CLIENT_ID` - Google OAuth ID
  - `DEBUG` - Debug mode flag

#### `desktop-app/requirements.txt`
- **Purpose**: Python package dependencies
- **Contains**: PyQt5, requests, python-dotenv

---

### **ROOT FILES**

#### `README.md`
- **Purpose**: This comprehensive project documentation
- **Contains**: Overview, features, setup, architecture, all file descriptions

#### `SETUP.md`
- **Purpose**: Step-by-step setup guide
- **Sections**: 
  - Prerequisites
  - Backend setup (install, .env, migrate, run)
  - Desktop setup (install, .env, run)
  - Web setup (install, .env, run)
  - Troubleshooting
  - How to get Google OAuth credentials

#### `run-all.sh`
- **Purpose**: Start all services at once
- **Command**: `./run-all.sh`
- **Starts**: Backend (port 8000) + Web (port 5000) + Desktop (separate window)

#### `run-backend.sh`
- **Purpose**: Start Django backend only
- **Command**: `./run-backend.sh`
- **Runs on**: `http://localhost:8000/api`

#### `run-web.sh`
- **Purpose**: Start React web frontend only
- **Command**: `./run-web.sh`
- **Runs on**: `http://localhost:5000`

#### `run-desktop.sh`
- **Purpose**: Start PyQt5 desktop app only
- **Command**: `./run-desktop.sh`
- **Connects to**: Backend at localhost:8000

#### `CLEANUP_REPORT.txt`
- **Purpose**: Documentation of cleaned up files
- **Details**: Lists 14 deleted files and why they were removed

---

## 🚀 SETUP INSTRUCTIONS

### **For Complete Setup, Visit**: [SETUP.md](./SETUP.md)

The setup guide contains everything you need:
- System prerequisites
- Step-by-step installation for each component
- Environment file templates
- Troubleshooting solutions
- Google OAuth credential setup

**Quick Reference:**
1. Clone the repository
2. Install dependencies for each component
3. Create `.env` files in `backend/`, `web/`, `desktop-app/`
4. Run migrations for Django
5. Start all services with `./run-all.sh`

---

## 📥 HOW TO CLONE & SETUP

### **Step 1: Clone from GitHub**

```bash
# Clone the repository
git clone https://github.com/your-username/chemizer-analytics.git

# Navigate to project directory
cd chemizer-analytics

# View the complete setup guide
cat SETUP.md
```

### **Step 2: Install Dependencies**

```bash
# Backend
cd backend
pip install -r requirements.txt

# Web Frontend
cd ../web
npm install

# Desktop
cd ../desktop-app
pip install -r requirements.txt
```

### **Step 3: Create Environment Files**

Create these 3 files in their respective folders (copy templates from SETUP.md):
- `backend/.env`
- `web/.env`
- `desktop-app/.env`

### **Step 4: Database Setup**

```bash
cd backend
python manage.py migrate
```

### **Step 5: Run Everything**

```bash
# From project root
./run-all.sh
```

---

## 🏃 HOW TO RUN (A TO Z)

### **Option 1: Start Everything at Once (RECOMMENDED)**

```bash
# From project root directory
./run-all.sh
```

This will automatically:
1. Start Django backend on `http://localhost:8000/api`
2. Start React web app on `http://localhost:5000`
3. Launch PyQt5 desktop app in a separate window

**Usage:**
- Open browser to `http://localhost:5000` for web app
- Desktop app window opens automatically
- Both connect to same backend on port 8000

### **Option 2: Manual Startup (3 Terminals)**

**Terminal 1 - Backend:**
```bash
./run-backend.sh
# Or: cd backend && python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - Web App:**
```bash
./run-web.sh
# Or: cd web && npm run dev
```

**Terminal 3 - Desktop App:**
```bash
./run-desktop.sh
# Or: cd desktop-app && python main.py
```

### **Usage Workflow**

1. **Register/Login**
   - Web: Enter email → Receive OTP → Verify → Dashboard
   - Desktop: Same flow in desktop interface
   - Both use same backend database

2. **Upload File**
   - Click upload area or drag-drop CSV/Excel file
   - View progress bar
   - File automatically analyzed

3. **View Results**
   - See interactive charts (7 types available)
   - Review data preview table
   - Download CSV or PDF report

4. **Manage Files**
   - Dashboard shows all uploaded files
   - Use 3-dot menu: View, Download, Delete, Share
   - Bulk operations available

5. **Profile Management**
   - View username and email
   - Change password
   - Download all data
   - Delete account (removes all data)

---

## 🏗️ ARCHITECTURE OVERVIEW

### **Application Flow**

```
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND LAYER                         │
├─────────────────────────────────────────────────────────┤
│  React Web (Port 5000)      │  PyQt5 Desktop          │
│  ─ Dashboard.tsx           │  ─ Main window          │
│  ─ Results.tsx             │  ─ Dashboard window     │
│  ─ Profile.tsx             │  ─ Results window       │
│  ─ Login.tsx               │  ─ Profile window       │
│                            │  ─ Session manager     │
└─────────────────────────────────────────────────────────┘
                          ↓↑ (HTTP/REST)
┌─────────────────────────────────────────────────────────┐
│              API LAYER (Django REST)                    │
├─────────────────────────────────────────────────────────┤
│  Backend Server (Port 8000)                            │
│  ─ Authentication endpoints                           │
│  ─ File upload endpoints                              │
│  ─ Analysis endpoints                                 │
│  ─ Profile endpoints                                  │
│  ─ Export endpoints (CSV/PDF)                         │
└─────────────────────────────────────────────────────────┘
                          ↓↑ (SQL)
┌─────────────────────────────────────────────────────────┐
│            DATA LAYER (SQLite/PostgreSQL)              │
├─────────────────────────────────────────────────────────┤
│  Database                                              │
│  ─ Users table                                        │
│  ─ Uploads table                                      │
│  ─ Results table                                      │
│  ─ Sessions table                                     │
└─────────────────────────────────────────────────────────┘
```

### **Authentication Flow**

```
1. User enters email → Backend generates OTP → Sends via Gmail SMTP
2. User receives OTP email → Enters OTP in app
3. Backend verifies OTP → Creates session token (JWT)
4. Token stored in browser (web) or ~/.chemizer (desktop)
5. All subsequent requests include token in header
6. Token expires after 48 hours (refreshable)
7. User can be auto-logged in on app restart (desktop)
```

### **File Upload & Analysis Flow**

```
1. User selects CSV/Excel file → Uploads to /upload endpoint
2. Backend receives file → Stores in media folder
3. pandas reads file → Performs analysis (stats, formatting)
4. Generates charts using data → Stores results in DB
5. Returns analysis to frontend → Displays charts & table
6. User can download CSV or generate PDF with all charts
7. All history stored in user's file list
```

---

## 🔌 API ENDPOINTS

### **Authentication**
```
POST   /auth/register       - Register new user
POST   /auth/verify-otp     - Verify OTP from email
POST   /auth/login          - Login with email/password
POST   /auth/logout         - Logout (invalidate token)
POST   /auth/refresh        - Refresh authentication token
```

### **File Management**
```
POST   /upload              - Upload and analyze file
GET    /files               - List all user's files
GET    /files/<id>          - Get specific file details
DELETE /files/<id>          - Delete uploaded file
GET    /files/download/<id> - Download file as CSV
```

### **Results & Analysis**
```
GET    /results/<id>        - Get analysis results for file
GET    /results/<id>/stats  - Get statistical analysis
GET    /results/<id>/pdf    - Generate and download PDF report
GET    /results/<id>/charts - Get all chart data
```

### **User Profile**
```
GET    /profile             - Get user profile info
PUT    /profile             - Update user profile
POST   /profile/password    - Change password
DELETE /profile             - Delete user account & all data
```

### **Bulk Operations**
```
POST   /bulk/download       - Download multiple files
POST   /bulk/delete         - Delete multiple files
POST   /bulk/export         - Export multiple analyses
```

### **Export**
```
POST   /export/csv          - Export data as CSV
POST   /export/pdf          - Export analysis as PDF
POST   /export/all          - Export everything
```

---

## 🔒 SECURITY FEATURES

- **Password Hashing**: bcrypt for secure password storage
- **Token-Based Auth**: JWT tokens with expiration
- **CORS Protection**: Restricted to localhost in dev, configured origins in prod
- **OTP Verification**: Time-limited one-time passwords
- **HTTPS Ready**: Can be configured for production SSL
- **Environment Secrets**: Sensitive data in .env files (never in code)
- **Session Timeout**: Automatic logout after inactivity
- **Data Privacy**: Users can delete all their data anytime

---

## 🤝 CONTRIBUTING

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature`
7. Create a Pull Request

---

## 📄 LICENSE

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 SUPPORT

For issues and questions:
1. Check [SETUP.md](./SETUP.md) troubleshooting section
2. Review error messages in console output
3. Verify all environment variables are set correctly
4. Ensure all dependencies are installed

---

## 🎉 QUICK START SUMMARY

```bash
# 1. Clone
git clone https://github.com/your-username/chemizer-analytics.git
cd chemizer-analytics

# 2. Setup (follow SETUP.md)
# - Install dependencies
# - Create .env files
# - Run migrations

# 3. Run everything
./run-all.sh

# 4. Access
# - Web: http://localhost:5000
# - Backend: http://localhost:8000/api
# - Desktop: Launches automatically

# 5. Login
# - Enter email → Receive OTP → Verify → Start using!
```

---

**Made with ❤️ for Chemical Data Analysis**

**Chemizer Analytics v1.0** | November 2025
