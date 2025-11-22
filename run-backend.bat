@echo off
cd backend
echo Starting Django Backend on port 8000...
python manage.py runserver 0.0.0.0:8000
pause
