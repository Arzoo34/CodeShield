@echo off
echo 🚀 Starting CodeShield...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Build and start services
echo 📦 Building and starting services...
docker-compose up --build -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
docker-compose ps | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo ✅ CodeShield is running!
    echo 🌐 Frontend: http://localhost:3000
    echo 🔧 Backend: http://localhost:5000
    echo 📊 API Health: http://localhost:5000/api/health
    echo.
    echo To stop: docker-compose down
    pause
) else (
    echo ❌ Failed to start services. Check logs with: docker-compose logs
    pause
    exit /b 1
)
