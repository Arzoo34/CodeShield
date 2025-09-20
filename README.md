# 🛡 CodeShield - Secure Code Execution Sandbox

A secure code execution platform that allows users to run code in isolated sandboxed environments. Built with Flask backend and modern web frontend.

## ✨ Features

- **Secure Code Execution**: Run Python and C++ code in isolated sandboxed environments
- **Resource Limits**: Time limits (30s) and memory restrictions to prevent system crashes
- **Real-time Results**: Get immediate feedback with execution time, output, and error messages
- **Modern UI**: Clean, responsive interface with syntax highlighting
- **Docker Containerization**: Safe execution environment using Docker containers
- **Multiple Languages**: Support for Python and C++ with proper compilation handling

## 🏗️ Project Structure

```
CodeShield/
├── frontend/                 # Static HTML/CSS frontend
│   ├── index.html           # Main HTML file
│   ├── projectos.html       # Project page
│   ├── styles.css           # Stylesheets
│   ├── Dockerfile           # Frontend container (nginx)
│   └── nginx.conf           # Nginx configuration
├── backend/                 # Backend API
│   ├── app.py              # Main Flask application
│   ├── sandbox_worker.py   # Code execution sandbox
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container
│   ├── templates/          # HTML templates
│   ├── submissions/        # User code submissions
│   └── logs/              # Application logs
├── docker-compose.yml      # Docker orchestration
├── .dockerignore          # Docker ignore file
├── .gitignore            # Git ignore file
├── start.sh              # Linux/Mac startup script
├── start.bat             # Windows startup script
└── README.md             # This file
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
The frontend consists of static HTML/CSS files served by nginx. Edit the files in the `frontend/` directory and rebuild the container.

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
    "language": "python",
    "stdin": ""
}
```

**Response:**
```json
{
    "submission_id": "uuid-string",
    "status": "completed",
    "result": {
        "verdict": "OK",
        "stdout": "Hello, World!\n",
        "stderr": "",
        "execution_time": 45.2,
        "success": true
    },
    "timestamp": "2024-01-01T12:00:00"
}
```

### Get Submission Status
```http
GET /api/status/{submission_id}
```

## 🎯 Supported Languages

### Python
- Direct execution with `python` interpreter
- Timeout: 30 seconds
- Memory limit: 512MB

### C++
- Compilation with `g++` compiler
- Compilation timeout: 10 seconds
- Execution timeout: 30 seconds
- Memory limit: 512MB

## 🔍 Verdict Types

- **OK**: Code executed successfully
- **TLE**: Time Limit Exceeded
- **RUNTIME_ERROR**: Runtime error during execution
- **CE**: Compilation Error (C++ only)
- **UNSUPPORTED_LANGUAGE**: Language not supported

## 🐳 Docker Configuration

### Backend Container
- **Base Image**: python:3.11-slim
- **Port**: 5000
- **Volumes**: submissions/, logs/

### Frontend Container
- **Base Image**: nginx:alpine
- **Port**: 80 (mapped to 3000)
- **Static Files**: HTML/CSS served via nginx

## 📝 Logging

Logs are stored in:
- **Application Logs**: `backend/logs/`
- **Docker Logs**: `docker-compose logs`

## 🧪 Testing

### Test the Application

1. **Start the application:**
   ```bash
   docker-compose up --build
   ```

2. **Access the frontend:**
   - Open http://localhost:3000
   - Click "Try Sandbox" or "Run code"

3. **Test Python code:**
   ```python
   print("Hello, World!")
   for i in range(5):
       print(f"Number: {i}")
   ```

4. **Test C++ code:**
   ```cpp
   #include <iostream>
   using namespace std;
   
   int main() {
       cout << "Hello, World!" << endl;
       for(int i = 0; i < 5; i++) {
           cout << "Number: " << i << endl;
       }
       return 0;
   }
   ```

5. **Test error handling:**
   ```python
   # This will cause a runtime error
   print(1/0)
   ```

6. **Test timeout:**
   ```python
   # This will cause TLE
   while True:
       pass
   ```

### Backend API Testing
```bash
# Health check
curl http://localhost:5000/api/health

# Submit Python code
curl -X POST http://localhost:5000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello, World!\")", "language": "python"}'

# Submit C++ code
curl -X POST http://localhost:5000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"code": "#include <iostream>\nint main(){std::cout<<\"Hello, World!\"<<std::endl;return 0;}", "language": "cpp"}'
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
