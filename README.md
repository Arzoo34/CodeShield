# CodeShield

A secure code execution platform that allows users to run code in isolated sandboxed environments. Built with Flask backend and modern web frontend.

## 🏗️ Project Structure

```
CodeShield/
├── frontend/                 # Frontend application
│   ├── index.html           # Main HTML file
│   ├── projectos.html       # Project page
│   ├── styles.css           # Stylesheets
│   └── (other UI assets)
├── backend/                 # Backend API
│   ├── app.py              # Main Flask application
│   ├── sandbox_worker.py   # Code execution sandbox
│   ├── requirements.txt    # Python dependencies
│   ├── templates/          # HTML templates
│   ├── submissions/        # User code submissions
│   └── logs/              # Application logs
├── docker-compose.yml      # Docker orchestration
├── Dockerfile(s)           # Container definitions
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Running the Application

#### Option 1: Using Shell Script (Linux/Mac)
```bash
./start.sh
```

#### Option 2: Using Batch File (Windows)
```cmd
start.bat
```

#### Option 3: Manual Docker Compose
```bash
docker-compose up --build
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 🛠️ Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

## 🔒 Security Features

- **Sandboxed Execution**: Code runs in isolated environments
- **Resource Limits**: CPU, memory, and time restrictions
- **Input Validation**: Comprehensive input sanitization
- **Logging**: Detailed execution logs
- **Container Security**: Non-root containers with minimal privileges

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```

### Code Submission
```http
POST /api/submit
Content-Type: application/json

{
    "code": "print('Hello, World!')",
    "language": "python"
}
```

## 🐳 Docker Configuration

### Backend Container
- **Base Image**: python:3.11-slim
- **Port**: 5000
- **Volumes**: submissions/, logs/

### Frontend Container
- **Base Image**: nginx:alpine
- **Port**: 80 (mapped to 3000)
- **Static Files**: Served via nginx

## 📝 Logging

Logs are stored in:
- **Application Logs**: `backend/logs/`
- **Docker Logs**: `docker-compose logs`

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Sandbox Testing
```python
from sandbox_worker import SandboxWorker

worker = SandboxWorker()
result = worker.execute_code("print('Hello!')", "python")
print(result)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

2. **Permission Issues**
   ```bash
   sudo chown -R $USER:$USER .
   ```

3. **Container Logs**
   ```bash
   docker-compose logs [service-name]
   ```

## 📞 Support

For support, please create an issue in the GitHub repository or contact the development team.

---

**CodeShield** - Secure Code Execution Platform
