# Blog API

This is a Blog API built with FastAPI. It supports user authentication, creating and managing blog posts, and more. The project uses PostgreSQL as the database and Alembic for database migrations. It is also containerized using Docker.

## Features

- User authentication (register, login)
- CRUD operations for blog posts
- Token-based authentication (JWT)
- Database migrations with Alembic
- Tests using Pytest

## Prerequisites

Before setting up the project, ensure you have the following installed:
- Python 3.11 or higher
- Docker and Docker Compose
- Poetry for dependency management (optional but recommended)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shyambista123/BlogAPI_FAST_API.git
cd BlogAPI_FAST_API
```

### 2. Install Dependencies

If you're using [Poetry](https://python-poetry.org/docs/#installation), run:

```bash
poetry install
```

Alternatively, you can install dependencies with `pip` if you are not using Poetry.

### 3. Setup Environment Variables

Create a `.env` and `.env.container` file in the project root directory. This file should include necessary configuration settings, such as the database URL and secret keys for JWT authentication. Here's an example or you can edit the .env.sample:

```
DATABASE_USERNAME="your_username"
DATABASE_PASSWORD="your_password"
DATABASE_PORT=5432
DATABASE_HOST="localhost"
DATABASE_NAME="your_database_name"
DATABASE_URL="postgresql://your_username:your_password@localhost:5432/your_database_name"
SECRET_KEY="your_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Database Setup

To create the database and run the migrations, you need to set up Alembic. Run the following command to apply the database migrations:

```bash
alembic upgrade head
```

This will set up the tables for users and posts.

### 5. Running the Application

#### Option 1: Using Docker

To run the app with Docker and Docker Compose, use:

```bash
docker-compose up --build
```

This will start the application, along with the PostgreSQL container.
#### Option 2: Without Docker (using Poetry)

To run the application without Docker, you can use Poetry to start the app. If you prefer using Uvicorn, run:

```bash
poetry run uvicorn main:app --reload
```

Or, if you prefer using the FastAPI CLI, run:

```bash
poetry run fastapi dev main.py
```

The application will be accessible at `http://localhost:8000/docs`.

### 6. Running Tests

You can run the tests using Pytest:

```bash
poetry run pytest
```

The tests are located in the `tests` directory, and you can add more as you develop the API further.

## Folder Structure

```
.
├── alembic.ini                  # Alembic configuration for database migrations
├── api                           # API route definitions (authentication, posts, users)
├── config                        # Configuration files (logging, settings)
├── db                            # Database-related files (models, migrations)
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Dockerfile to build the app container
├── main.py                       # FastAPI application entry point
├── models                        # ORM models (user, post)
├── schemas                       # Pydantic models for request/response validation
├── services                      # Business logic layer (auth, posts, users)
├── tests                         # Unit and integration tests for the API
├── pyproject.toml                # Poetry configuration for dependency management
└── README.md                     # Project documentation
```

## API Endpoints

- `POST /auth/register`: Create a new user
- `POST /auth/login`: Log in and receive a JWT token
- `GET /api/posts`: Retrieve all blog posts (authentication required)
- `POST /api/posts`: Create a new blog post (authentication required)
- `GET /api/posts/{id}`: Retrieve a specific blog post (authentication required)
- `PUT /api/posts/{id}`: Update a specific blog post (authentication required)
- `DELETE /posts/{id}`: Delete a specific blog post (authentication required)