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

- **Django 5.2+** with Django REST Framework 3.16+
- **Python 3.13** with `uv` package manager for fast dependency management
- **Containerized deployment** with Docker and Docker Compose
- **Background tasks** with Celery 5.5+ and Redis 8.0+
- **Database** PostgreSQL 17+ (production) / SQLite (development)
- **Authentication** JWT-based with django-simple-jwt 5.4
- **Code quality** Pre-commit hooks, Ruff linting, and coverage reporting
- **Monitoring** Sentry integration for error tracking and performance monitoring
- **CI/CD** GitHub Actions workflows with automated releases and dependabot
- **Production-ready** Gunicorn WSGI server with health checks and optimizations
- **Advanced logging** with Loguru for structured logging
- **Docker health checks** for all services with proper service dependencies

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

4. **Set up environment variables** (optional for development):
    ```bash
    # Create .env file for custom configuration
    # Development uses SQLite by default, no additional setup needed
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
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOST=your-domain.com,localhost

   # Database Configuration
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=app
   SQL_USER=postgres
   SQL_PASSWORD=secure-password
   SQL_HOST=db
   SQL_PORT=5432

   # Redis Configuration
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_BACKEND_URL=redis://redis:6379/0
   CACHE_LOCATION_URL=redis://redis:6379/1

   # Optional: CORS and performance settings
   CORS_ORIGIN_WHITELIST=https://your-frontend.com
   ENTRY_PORT=15000
   GUNICORN_WORKERS=4
   CELERY_CONCURRENCY=4
   ```

2. **Deploy with Docker Compose**:
   ```bash
   docker compose up -d --build
   ```

## 📁 Project Structure

```
.
├── core/                     # Django project configuration
│   ├── settings/            # Environment-specific settings
│   │   ├── common.py        # Shared settings
│   │   ├── dev.py           # Development settings
│   │   ├── prod.py          # Production settings
│   │   └── version.py       # Version management
│   ├── celery/              # Celery configuration
│   ├── utils/               # Shared utilities
│   │   ├── logger.py        # Loguru logging setup
│   │   ├── pagination.py    # Custom pagination
│   │   └── urls.py          # Health check and auth endpoints
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── user/                    # User application
│   ├── functions/           # Business logic utilities
│   ├── migrations/          # Database migrations
│   ├── orm/                 # ORM utilities and managers
│   ├── services/            # Service layer
│   ├── tests/               # Application tests
│   ├── models.py            # User models
│   ├── serializers.py       # API serializers
│   ├── views.py             # API views
│   ├── tasks.py             # Celery tasks
│   └── urls.py              # User API endpoints
├── data/                    # Persistent data (mounted in Docker)
│   ├── logs/                # Application logs
│   ├── media/               # User uploaded files
│   ├── static/              # Collected static files
│   └── db.sqlite3           # SQLite database (dev only)
├── static/                  # Static assets source
├── .github/                 # GitHub Actions workflows
│   ├── workflows/
│   │   ├── ci.yaml          # Continuous integration
│   │   └── release.yaml     # Automated releases
│   └── dependabot.yaml      # Dependency updates
├── docker-compose.yaml      # Docker services configuration
├── Dockerfile               # Multi-stage container build
├── Makefile                 # Development commands
├── pyproject.toml           # Dependencies and tools config
├── uv.lock                  # Locked dependencies
├── wait-for                 # Service dependency script
├── version.json             # Project version (1.5.7)
└── README.md                # This file
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
make celery               # Start Celery workers with optional beat
make test                 # Run tests with database preservation
make coverage             # Run tests with coverage report
make lint                 # Run pre-commit hooks (linting)
make collectstatic        # Collect static files
```

### Short Commands (Aliases)
```bash
make r                    # Short for 'run'
make m                    # Short for 'migrate'
make mm                   # Short for 'makemigrations'
make mr                   # Run migrate then run server
```

### Production Commands
```bash
make prod-migrate         # Run migrations in production (with service wait-for)
make prod-gunicorn        # Start production web server with optimizations
make prod-celery          # Start production Celery workers
```

### Utility Commands
```bash
make secret              # Generate Django secret key
make compilemessages     # Compile translation messages
make help                # Show all available commands with descriptions
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

The project is configured for high test coverage with the following settings:
- Minimum coverage: 50%
- Excludes migrations, tests, and settings from coverage
- Uses `--keepdb` for faster test runs

## 📦 Key Dependencies

### Core Framework
- **Django 5.2+**: Modern web framework
- **Django REST Framework 3.16+**: Powerful API development
- **django-simple-jwt 5.4**: JWT authentication with token rotation
- **django-cors-headers 4.7+**: CORS handling for frontend integration
- **django-filter 25.1+**: Advanced filtering for APIs
- **django-extensions 4.1+**: Additional management commands

### Background Tasks & Caching
- **Celery 5.5+**: Distributed task queue with beat scheduling
- **Redis 8.0+**: High-performance message broker and cache backend

### Database & Storage
- **psycopg 3.2+**: Modern PostgreSQL adapter with binary support
- **django-environ 0.12+**: Environment variable management

### Production & Monitoring
- **Gunicorn 23.0+**: Production WSGI server with worker management
- **Sentry SDK 2.29+**: Error monitoring and performance tracking
- **Loguru 0.7+**: Advanced structured logging
- **air-drf-relation 0.6+**: Enhanced DRF relationship handling

### Development Tools
- **Ruff 0.11+**: Fast Python linter and formatter (replaces flake8, black, isort)
- **pre-commit 4.2+**: Git hooks framework for code quality
- **coverage 7.8+**: Code coverage measurement with reporting
- **uv**: Ultra-fast Python package manager

## 🔒 Security Features

- **Environment-based configuration** with `django-environ`
- **JWT authentication** with automatic token rotation and refresh
- **CORS protection** with configurable origin whitelist
- **Security middleware** enabled with Django defaults
- **Password validation** with comprehensive validators
- **Sentry integration** for error monitoring and alerting
- **Docker health checks** ensuring service availability
- **Non-root container execution** for enhanced security

## 🏗️ CI/CD & Automation

The project includes comprehensive GitHub Actions workflows:

### Available Workflows
- **CI Pipeline** (`.github/workflows/ci.yaml`):
  - Runs tests across multiple Python versions
  - Linting with Ruff
  - Code coverage reporting
  - Django migrations check

- **Release Pipeline** (`.github/workflows/release.yaml`):
  - Automated semantic versioning
  - Changelog generation
  - GitHub releases creation
  - Docker image building and publishing

- **Dependabot** (`.github/dependabot.yaml`):
  - Automated dependency updates for Python packages
  - Docker base image updates
  - Security vulnerability patches

### Environment Variables for CI/CD
Configure these secrets in your GitHub repository:
- `SENTRY_DSN`: For error monitoring
- `DOCKER_REGISTRY_TOKEN`: For container registry access

## 📝 API Documentation

### Available Endpoints
- **Health Check**: `GET /api/v1/ready` - Service health status
- **Authentication**:
  - `POST /api/v1/token/` - Obtain JWT token pair
  - `POST /api/v1/token/refresh/` - Refresh access token
- **User Management**: `api/v1/users/` - RESTful user operations

### API Features
- JWT-based authentication with automatic token rotation
- Standardized JSON responses
- Request/response filtering with django-filter
- Custom pagination with configurable page sizes
- CORS support for frontend integration

## 🐳 Docker Configuration

### Multi-stage Build
The Dockerfile uses a multi-stage build approach:
1. **Builder stage**: Installs dependencies with uv
2. **Runtime stage**: Minimal Python image with compiled dependencies

### Services Architecture
- **app**: Main Django application with health checks
- **celery**: Background task workers with dependency on app health
- **redis**: Message broker and cache with data persistence
- **db**: PostgreSQL database with optimized configuration

### Health Checks
All services include comprehensive health checks:
- Application health via HTTP endpoint
- Redis ping checks
- PostgreSQL connection verification
- Automatic service restart on failure

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG` | Enable debug mode | `True` | No |
| `SECRET_KEY` | Django secret key | - | Yes (production) |
| `ALLOWED_HOST` | Allowed hostnames | `*` | No |
| `SQL_ENGINE` | Database engine | SQLite | No |
| `CELERY_BROKER_URL` | Celery broker URL | - | No |
| `CACHE_LOCATION_URL` | Redis cache URL | Database cache | No |
| `ENTRY_PORT` | External port | `15000` | No |
| `GUNICORN_WORKERS` | Gunicorn workers | `4` | No |
| `CELERY_CONCURRENCY` | Celery concurrency | `4` | No |

### Performance Tuning
The production setup includes:
- Gunicorn with multiple workers and request limits
- PostgreSQL with optimized connection and memory settings
- Redis with persistent data storage
- Celery with configurable concurrency and beat scheduling

## 🤝 Contributing

1. **Install development dependencies**:
   ```bash
   uv sync
   ```

2. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

3. **Run tests**:
   ```bash
   make test
   ```

4. **Check linting**:
   ```bash
   make lint
   ```

5. **Check coverage**:
   ```bash
   make coverage
   ```

### Code Quality Standards
- **Linting**: Ruff for fast Python linting and formatting
- **Testing**: Maintain >50% code coverage
- **Documentation**: Update README for significant changes
- **Versioning**: Follow semantic versioning principles

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🔗 Resources

- [Django Documentation](https://docs.djangoproject.com/) - Official Django docs
- [Django REST Framework](https://www.django-rest-framework.org/) - DRF documentation
- [Celery Documentation](https://docs.celeryproject.org/) - Background task processing
- [uv Documentation](https://docs.astral.sh/uv/) - Fast Python package manager
- [Docker Documentation](https://docs.docker.com/) - Container platform
- [Ruff Documentation](https://docs.astral.sh/ruff/) - Python linter and formatter
