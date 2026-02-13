FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-interaction --no-root

# App Code
COPY . .

EXPOSE 8501

# Default command (can be overridden at run time)
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]