# Use the official Python 3.13 slim image as the base
FROM python:3.13-slim AS builder

# Install system dependencies required for compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Install UV - a modern Python package manager
COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /uvx /bin/

# Create working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create virtual environment and install dependencies
RUN uv sync --frozen --no-dev --no-cache

# Final stage for production
FROM python:3.13-slim

# Install runtime-only dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    netcat-openbsd \
    make \
    # gettext \ # Uncomment this when we need it
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy UV into the final image
COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /uvx /bin/

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy wait-for script and make it executable
COPY wait-for /usr/local/bin/wait-for
RUN chmod +x /usr/local/bin/wait-for

# Copy application source code
COPY . .

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables for Python and Django
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app
# DJANGO_SETTINGS_MODULE=core.settings.prod

# Create necessary directories for Django
RUN mkdir -p /app/data/static /app/data/media

# Expose port 8000
EXPOSE 8000

# Run Django with Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
