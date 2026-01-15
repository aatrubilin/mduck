# Use an official Python runtime as a parent image
FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1

# Set work directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry dependency files
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry install --no-root --without dev

# Copy the rest of the application code
COPY src/ /app/src

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "api", "--host", "0.0.0.0", "--port", "8000"]
