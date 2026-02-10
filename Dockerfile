# Use a slim Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies for building Glucose
RUN apt-get update && apt-get install -y \
    build-essential \
    zlib1g-dev \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and install Glucose SAT solver
RUN wget https://github.com/audemard/glucose/archive/refs/tags/4.2.1.tar.gz -O glucose.tar.gz \
    && tar -xvf glucose.tar.gz \
    && mv glucose-4.2.1 glucose \
    && rm glucose.tar.gz \
    && cd glucose/simp \
    && make

# Create necessary directories for runtime data
RUN mkdir -p data/in data/out

# Copy application code
COPY src/ src/
COPY data/ data/

# Expose port
EXPOSE 4200

# Start the application
CMD ["uvicorn", "src.core.server:app", "--host", "0.0.0.0", "--port", "4200"]
