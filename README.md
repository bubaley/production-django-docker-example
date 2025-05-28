# Django Production-Ready Template

A production-ready Django project template built with Python 3.13, featuring modern tooling and containerized deployment. This template includes integrations with Celery for background tasks, Redis for caching and message brokering, PostgreSQL for the database, and comprehensive development tooling.

## ⚠️ **IMPORTANT: Template Version Tracking**

**For proper template maintenance and updates, add the following comments at the very beginning of your `core/settings/common.py` file:**

```python
# https://github.com/bubaley/production-django-docker-example
# version: 0.0.0 | Increase the version after changes from the template, this will make it easier to make new ones
```

This practice helps you:
- 🔄 **Track template updates** and know which version you're using
- 📊 **Compare changes** when new template versions are released  
- 🚀 **Easier migration** to newer template versions
- 📝 **Document customizations** made to the base template

**Remember to increment the version number whenever you make significant changes to maintain clear version history.**

## 🚀 Features

- **Django 5.2+** with Django REST Framework
- **Python 3.13** with `uv` package manager for fast dependency management
- **Containerized deployment** with Docker and Docker Compose
- **Background tasks** with Celery and Redis
- **Database** PostgreSQL (production) / SQLite (development)
- **Authentication** JWT-based with django-simple-jwt
- **Code quality** Pre-commit hooks, Ruff linting, and coverage reporting
- **Monitoring** Sentry integration for error tracking
- **CI/CD** GitHub Actions workflows included
- **Production-ready** Gunicorn WSGI server with health checks

## 📋 Prerequisites

- **Python**: 3.13
- **uv**: Fast Python package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Docker & Docker Compose**: For containerized deployment
- **Make**: For running development commands

## 🛠️ Quick Start

### Local Development

1. **Clone the repository**:
    ```bash
    git clone https://github.com/bubaley/production-django-docker-example
    cd production-django-docker-example
    ```

2. **Create virtual environment**:
    ```bash
    uv venv --python 3.13
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    uv sync
    ```

4. **Set up environment variables**:
    ```bash
    cp .env.example .env  # Create .env file and configure your settings
    ```

5. **Initialize database**:
    ```bash
    make migrate
    ```

6. **Create superuser** (optional):
    ```bash
    make createsuperuser
    ```

7. **Run development server**:
    ```bash
    make run
    ```

The application will be available at `http://localhost:8000`.

### Docker Development

1. **Start all services**:
    ```bash
    docker compose up --build
    ```

2. **Access the application**:
   - API: `http://localhost:15000` (or your configured `ENTRY_PORT`)
   - Health check: `http://localhost:15000/api/v1/ready`

### Production Deployment

1. **Configure environment variables** in `.env`:
   ```bash
   DEBUG=False
   SECRET_KEY=example-secret-key
   ALLOWED_HOST=*
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=app
   SQL_USER=postgres
   SQL_PASSWORD=postgres
   SQL_HOST=db
   SQL_PORT=5432
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_BACKEND_URL=redis://redis:6379/0
   CACHE_LOCATION_URL=redis://redis:6379/1
   ```

2. **Deploy with Docker Compose**:
   ```bash
   docker compose up -d --build
   ```

## 📁 Project Structure

```
.
├── core/                   # Django project configuration
│   ├── settings/          # Environment-specific settings
│   │   ├── common.py      # Shared settings
│   │   ├── dev.py         # Development settings
│   │   └── prod.py        # Production settings
│   ├── celery/            # Celery configuration
│   └── utils/             # Shared utilities
├── user/                  # User application
│   ├── models.py          # User models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── tasks.py           # Celery tasks
│   └── ...
├── data/                  # Persistent data (mounted in Docker)
│   ├── logs/              # Application logs
│   ├── media/             # User uploaded files
│   ├── static/            # Static files
│   └── db.sqlite3         # SQLite database (dev only)
├── .github/               # GitHub Actions workflows
├── docker-compose.yaml    # Docker services configuration
├── Dockerfile             # Container build instructions
├── Makefile              # Development commands
├── pyproject.toml        # Project dependencies and tools config
└── README.md             # This file
```

## 🔧 Available Commands

The project includes a comprehensive Makefile with shortcuts:

### Development Commands
```bash
make run                  # Start development server
make shell                # Open Django shell with shell_plus
make migrate              # Run database migrations
make makemigrations       # Create new migrations
make createsuperuser      # Create Django superuser
make gunicorn             # Start Gunicorn server
make celery               # Start Celery workers
make test                 # Run tests with database preservation
make coverage             # Run tests with coverage report
make lint                 # Run pre-commit hooks (linting)
```

### Production Commands
```bash
make prod-migrate         # Run migrations in production (with service wait-for)
make prod-gunicorn        # Start production web server
make prod-celery          # Start production Celery workers
```

### Utility Commands
```bash
make secret              # Generate Django secret key
make compilemessages     # Compile translation messages
make help                # Show all available commands
```

## 🧪 Testing

Run the test suite:
```bash
make test
```

Run tests with coverage:
```bash
make coverage
```

## 📦 Key Dependencies

### Core Framework
- **Django 5.2+**: Web framework
- **Django REST Framework 3.16+**: API development
- **django-simple-jwt 5.5+**: JWT authentication
- **django-cors-headers**: CORS handling
- **django-filter**: Advanced filtering for APIs

### Background Tasks & Caching
- **Celery 5.5+**: Distributed task queue
- **Redis 6.2+**: Message broker and cache backend

### Database & Storage
- **psycopg 3.2+**: PostgreSQL adapter
- **django-environ**: Environment variable management

### Production & Monitoring
- **Gunicorn 23.0+**: WSGI HTTP server
- **Sentry SDK 2.29+**: Error monitoring and performance tracking
- **Loguru 0.7+**: Advanced logging

### Development Tools
- **Ruff 0.11+**: Fast Python linter and formatter
- **pre-commit 4.2+**: Git hooks framework
- **coverage 7.8+**: Code coverage measurement
- **django-extensions**: Additional Django management commands

## 🔒 Security Features

- Environment-based configuration with `django-environ`
- JWT-based authentication with token rotation
- CORS protection configured
- Security middleware enabled
- Sentry integration for error monitoring
- Docker health checks

## 🏗️ CI/CD

The project includes GitHub Actions workflows:

- **CI Pipeline** (`.github/workflows/ci.yaml`): Runs tests and linting
- **Release Pipeline** (`.github/workflows/release.yaml`): Automated releases
- **Docker Build** (`.github/workflows/docker.yaml.example`): Container builds
- **Dependabot** (`.github/dependabot.yaml`): Automated dependency updates

## 📝 API Documentation

The API includes:
- User authentication endpoints
- Health check endpoint (`/api/v1/ready`)
- RESTful user management
- JWT token authentication

## 🤝 Contributing

1. Install development dependencies: `uv sync`
2. Set up pre-commit hooks: `pre-commit install`
3. Run tests: `make test`
4. Check linting: `make lint`

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🔗 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Docker Documentation](https://docs.docker.com/)
