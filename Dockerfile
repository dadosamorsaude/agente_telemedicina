# Use official uv image as builder
FROM astral-sh/uv:python3.12-bookworm-slim AS builder

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

# Copy lockfile and project description
COPY uv.lock pyproject.toml /app/

# Install dependencies (cached)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Final runtime stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy virtual environment and application code
COPY --from=builder /app/.venv /app/.venv
COPY . /app

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port (Render uses PORT env, default 10000)
EXPOSE 10000

# Start Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
