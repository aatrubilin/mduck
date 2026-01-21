# ---- Base Stage ----
FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# ---- Builder Stage ----
FROM base AS builder

WORKDIR /app

# Copy only dependency definition file to leverage caching
COPY requirements.txt /app/

# Install dependencies using pip. This layer will be cached.
RUN pip install -r requirements.txt

# Copy the rest of the files needed for the project installation
COPY poetry.lock pyproject.toml README.md /app/
COPY src/ /app/src/

# Install the project itself. Poetry will recognize that the
# dependencies are already installed, so this step will be very fast.
RUN poetry install --only main

# ---- Final Stage ----
FROM python:3.14-slim AS final

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Create log directory and set permissions
RUN mkdir -p /var/log/mduck && chown app:app /var/log/mduck

# Copy installed dependencies and scripts from the builder stage
COPY --from=builder /usr/local/lib/python3.14/site-packages/ /usr/local/lib/python3.14/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
# Copy the application code
COPY --from=builder /app/src/ /app/src/

# Switch to the non-root user
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/healthcheck || exit 1

ENTRYPOINT ["run-webhook"]
CMD ["--host", "0.0.0.0", \
    "--port", "8000", \
    "--log-level", "info", \
    "--log-format", "human", \
    "--log-file", "/var/log/mduck/mduck.log"]
