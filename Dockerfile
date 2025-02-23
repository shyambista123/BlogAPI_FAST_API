# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry using pip (this is a more reliable method for installation in Docker)
RUN pip install --no-cache-dir poetry

# Verify that poetry is installed successfully
RUN poetry --version

# Copy poetry lock files and pyproject.toml first to cache dependencies
COPY pyproject.toml poetry.lock /app/

# Install dependencies using poetry
RUN poetry install --no-interaction --no-root

# Copy the rest of the application code into the container
COPY . /app/

# Command to run the FastAPI application using the official FastAPI CLI
CMD ["poetry", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
