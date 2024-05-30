FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
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

# Start PostgreSQL and perform database setup
RUN /etc/init.d/postgresql start && \
    service postgresql start && \
    su - postgres -c "psql -c \"CREATE DATABASE $POSTGRES_DB\"" && \
    su - postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD'\"" && \
    su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER\""

# Expose the PostgreSQL port
EXPOSE 5432

# Clean up
RUN apt-get clean

# Run the FastAPI application
CMD service postgresql start && uvicorn app.core.main:app --host 0.0.0.0 --port 8000