# Django Project Template

This is a Django project template using Python 3.12, designed for easy local and Docker-based deployment. It includes integrations with Celery, Redis, PostgreSQL, and Sentry, and uses `uv` as the package manager for optimized dependency management. The configuration is organized within `pyproject.toml` for both application and development dependencies.

## Prerequisites

- **Python**: 3.12
- **Docker**: For containerized deployment (optional but recommended)
- **uv**: Fast package manager ([uv documentation](https://docs.astral.sh/uv/))

## Quick Start

### Local Development Setup

1. **Initialize Virtual Environment**:
    ```bash
    uv venv --python 3.12
    ```

2. **Activate the Environment**:
    ```bash
    source .venv/bin/activate
    ```

3. **Initialize the Project**:
    ```bash
    . ./scripts/init_project.sh
    ```

4. **Set Up Database Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the Server**:
    ```bash
    python manage.py runserver
    ```

### Docker-Based Deployment

1. **Build and Run Containers**:
    ```bash
    docker compose up --build
    ```

    This will spin up services including Django, Celery, Redis, and PostgreSQL as configured in `docker-compose.yml`.

2. **Environment Configuration**:
   Ensure that `.env` exists in the project root and contains all necessary environment variables.

### Project Structure

- **Core Applications**: Django with DRF, Celery, Redis, and PostgreSQL integrations
- **Package Manager**: `uv` for optimized builds
- **Configuration**: Defined in `pyproject.toml` and `.env`
- **Logs, Media, and Static Files**: Mapped to the `data` directory for easy mounting and persistence
- **Celery**: Configured in `core/celery.py`, with startup handled via `scripts/start_celery.sh`

## Key Dependencies

The project uses the following main dependencies:

- **Django**: Main framework
- **Django Rest Framework**: API development
- **Gunicorn**: WSGI HTTP server
- **django-environ**: Environment variable management
- **Django Simple JWT**: JSON Web Token-based authentication
- **Sentry SDK**: Error monitoring
- **Django Filter**: Filtering support for DRF
- **Celery**: Background task queue
- **Redis**: In-memory data structure store (used as a broker for Celery)
- **Air DRF Relation**: Enhanced relation support for DRF serializers

### Development Dependencies

- **Ruff**: Python linter for fast code analysis
- **pre-commit**: Git hook manager

## Important Notes

- **Data Persistence**: `logs`, `media`, `static`, and `db.sqlite3` are stored in the `data` directory for easy mounting with Docker volumes.
- **Celery Configuration**: Located in `core/celery.py`. Use `scripts/start_celery.sh` to start Celery tasks.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
