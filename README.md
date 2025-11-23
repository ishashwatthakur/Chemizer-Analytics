# 🧪 CHEMIZER ANALYTICS

**Professional Chemical Equipment Data Analysis Platform**

A comprehensive web and desktop application for analyzing chemical equipment data from CSV/Excel files, generating detailed reports with visualizations, and managing analyzed data through a secure authentication system.

---

**Heads Up! We're connecting to our live server (Render). Please allow an extra few seconds for the results to load.**

---
## 📋 TABLE OF CONTENTS

- [About](#about)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)

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
- **Intuitive Navigation** - Easy-to-use dashboard and workflows
- **Real-time Updates** - Instant feedback on operations

---

## 🛠️ TECHNOLOGY STACK

### **Backend**
| Technology | Purpose |
|------------|---------|
| Django | Web framework & core backend |
| Django REST Framework | RESTful API building |
| django-allauth | User authentication & OAuth |
| pandas | CSV/Excel file processing |
| ReportLab | PDF generation with charts |
| PostgreSQL/SQLite | Database |

### **Web Frontend**
| Technology | Purpose |
|------------|---------|
| React 18 | Component-based UI |
| Vite | Build tool & dev server |
| TypeScript | Type-safe development |
| Tailwind CSS | Styling |
| Recharts | Interactive charts |

### **Desktop Application**
| Technology | Purpose |
|------------|---------|
| PyQt5 | Native desktop UI |
| requests | API communication |
| python-dotenv | Configuration management |

---

## 📁 PROJECT STRUCTURE

```
chemizer-analytics/
├── README.md                    # Project overview (this file)
├── SETUP.md                     # Complete setup guide ⭐ START HERE
├── backend/                     # Django backend
│   ├── manage.py              # Django management tool
│   ├── requirements.txt        # Python dependencies
│   ├── db.sqlite3             # Database (auto-created by migrations)
│   └── .env                   # Environment variables (you create this)
├── web/                        # React + Vite frontend
│   ├── package.json           # Node dependencies
│   └── .env                   # Environment variables (you create this)
├── desktop-app/               # PyQt5 desktop application
│   ├── main.py               # Entry point
│   ├── requirements.txt        # Python dependencies
│   └── .env                   # Environment variables (you create this)
└── pyrightconfig.json          # Type checking configuration
```

---

## 🚀 SETUP INSTRUCTIONS

### **⭐ FOR COMPLETE SETUP, READ: [SETUP.md](./SETUP.md)**

The setup guide includes:
- **Manual step-by-step commands** for Windows, Mac, and Linux
- **Database setup explanation** (how db.sqlite3 is created)
- **Environment file templates** and examples
- **Google OAuth credential configuration**
- **Troubleshooting solutions**

**Quick Summary:**
1. Clone the repository
2. Follow [SETUP.md](./SETUP.md) for detailed manual instructions
3. Install dependencies for each component
4. Create `.env` files in `backend/`, `web/`, `desktop-app/`
5. Run Django migrations (creates database automatically)
6. Start all services manually in separate terminals

---

## 🏃 QUICK START - MANUAL COMMANDS

### **Open 3 Separate Terminal Windows**

**Terminal 1 - Backend Server:**
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - Web Frontend:**
```bash
cd web
npm run dev
```

**Terminal 3 - Desktop Application:**
```bash
cd desktop-app
python main.py
```

---

## 🏗️ ARCHITECTURE OVERVIEW

### **System Architecture**

```
┌─────────────────────────────────────────────────────┐
│            FRONTEND LAYER                           │
│  ┌──────────────────┐        ┌──────────────────┐   │
│  │  Web App (React) │        │ Desktop (PyQt5)  │   │
│  │   Port: 5000     │        │  Native App      │   │
│  └────────┬─────────┘        └────────┬─────────┘   │
└───────────┼─────────────────────────────┼────────────┘
            │                             │
            │         HTTP/REST          │
            └─────────────┬───────────────┘
                          │
┌─────────────────────────┴─────────────────────────┐
│          BACKEND LAYER (Django)                   │
│  ┌──────────────────────────────────────────┐     │
│  │   REST API Endpoints                     │     │
│  │   - Authentication (OTP, OAuth, Login)   │     │
│  │   - File Upload & Processing             │     │
│  │   - Analysis & Visualization             │     │
│  │   - PDF Report Generation                │     │
│  │   - User Management                      │     │
│  └────────────────┬─────────────────────────┘     │
│                   │                               │
│  ┌────────────────▼─────────────────────────┐     │
│  │   Database (SQLite: db.sqlite3)          │     │
│  │   - Users & Authentication               │     │
│  │   - Upload History & Metadata            │     │
│  │   - Session Data (48-hour persistence)   │     │
│  └──────────────────────────────────────────┘     │
└──────────────────────────────────────────────────┘
```

### **Data Flow**

```
User Upload → Backend Processing → Chart Generation → 
PDF Creation → Storage → Download to User
```

---

## 🔗 Important Links

- **Setup Guide**: [SETUP.md](./SETUP.md) - Complete manual setup instructions
- **GitHub**: [Repository](https://github.com/ishashwatthakur/Chemizer-Analytics)
- **Issues**: Report bugs or request features

---

## 📝 LICENSE

This project is open source and available under the MIT License.

---

**Made with Love for Chemical Data Analysis**

**Chemizer Analytics ** 
