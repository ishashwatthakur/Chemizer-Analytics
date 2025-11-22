@echo off
echo Starting all services...
echo.
echo Terminal 1: Starting Backend...
start cmd /k "cd backend && python manage.py runserver 0.0.0.0:8000"
echo.
timeout /t 3 /nobreak
echo Terminal 2: Starting Web...
start cmd /k "cd web && npm run dev"
echo.
timeout /t 2 /nobreak
echo Terminal 3: Starting Desktop...
start cmd /k "cd desktop-app && python main.py"
echo.
echo All services started!
pause
