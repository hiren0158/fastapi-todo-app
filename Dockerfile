FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ToDoApp2 ./ToDoApp2

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8081

# Run the application
CMD ["uvicorn", "ToDoApp2.main:app", "--host", "0.0.0.0", "--port", "8081"]
