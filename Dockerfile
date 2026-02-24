FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev dependencies, no project itself yet)
RUN uv sync --frozen --no-install-project --no-dev

# Copy application source
COPY . .

# Install project
RUN uv sync --frozen --no-dev

# Collect static files (SECRET_KEY is required by Django even for collectstatic)
RUN SECRET_KEY=build-placeholder DATABASE_URL=sqlite:///tmp/build.db \
    uv run python manage.py collectstatic --noinput

EXPOSE 8000

# Run gunicorn; use exec form so signals are forwarded correctly
CMD ["uv", "run", "gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "60"]
