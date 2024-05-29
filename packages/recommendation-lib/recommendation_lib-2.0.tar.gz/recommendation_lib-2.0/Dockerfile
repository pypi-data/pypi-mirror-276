# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
# Install gcc and other dependencies for building psycopg2
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Install PostgreSQL
RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=gpanagou
ENV POSTGRES_PASSWORD=my_secret_password
ENV POSTGRES_DB=htb

# Initialize PostgreSQL database
RUN /etc/init.d/postgresql start && \
    service postgresql start && \
    su - postgres -c "psql -c \"SELECT 'CREATE DATABASE $POSTGRES_DB' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB')\"" && \
    su - postgres -c "psql -c \"SELECT 'CREATE USER $POSTGRES_USER WITH PASSWORD ''' || '$POSTGRES_PASSWORD' || '''' WHERE NOT EXISTS (SELECT FROM pg_user WHERE usename = '$POSTGRES_USER')\"" && \
    su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER\""

# Run the FastAPI application
CMD ["uvicorn", "app.core.main:app", "--host", "0.0.0.0", "--port", "8000"]