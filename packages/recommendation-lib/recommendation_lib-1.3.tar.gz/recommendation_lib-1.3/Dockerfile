# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev && \
    pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Install PostgreSQL client for database operations
RUN apt-get update && apt-get install -y postgresql-client

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=my_secret_password
ENV POSTGRES_DB=postgres

# Copy initialization script
# COPY init.sql /docker-entrypoint-initdb.d/

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]