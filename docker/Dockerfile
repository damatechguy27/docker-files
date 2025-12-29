FROM python:3.11-slim

# Set working directory
WORKDIR /opt/dagster/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create dagster home directory
RUN mkdir -p /opt/dagster/dagster_home

# Copy configuration files to DAGSTER_HOME
COPY dagster.yaml /opt/dagster/dagster_home/dagster.yaml

# Copy workspace config to working directory
COPY workspace.yaml .

# Copy application code
COPY dagster_project/ ./dagster_project/

# Create data directory
RUN mkdir -p /opt/dagster/app/data

# Set environment variables
ENV DAGSTER_HOME=/opt/dagster/dagster_home
ENV PYTHONPATH="/opt/dagster/app:${PYTHONPATH}"

# Expose ports
EXPOSE 3000 4000
