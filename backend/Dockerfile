FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Node.js and JDK
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    nodejs \
    npm \
    openjdk-21-jdk \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
