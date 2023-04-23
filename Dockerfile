# Use the official Python base image
FROM python:3.10

# Install system dependencies and Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --upgrade pip \
    && pip install --no-cache-dir poetry

# Configure Poetry
ENV POETRY_VERSION=1.1.12 
ENV POETRY_HOME="/opt/poetry" 
ENV POETRY_NO_INTERACTION=1 
ENV POETRY_VIRTUALENVS_CREATE=false 
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copy pyproject.toml and poetry.lock files
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Install package dependencies with Poetry
RUN poetry install --no-root

# Copy the rest of your application code
COPY . .

# Build the package
RUN poetry build

# Second stage: run the FastAPI application
FROM python:3.10

# Copy the package from the builder stage
COPY --from=builder /app/dist /app/dist

# Install the package
# Install Uvicorn for running the FastAPI application
RUN pip install --no-cache-dir /app/dist/*.tar.gz \ 
    && pip install --no-cache-dir uvicorn

# Expose the port for the FastAPI application
EXPOSE 8000

# Set the entrypoint for the container
ENTRYPOINT ["uvicorn", "pantry.main:app", "--host", "0.0.0.0", "--port", "8000"]