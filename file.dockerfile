# Use an official lightweight Python runtime
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency definition first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to execute pipeline on container startup
CMD ["python", "main.py"]