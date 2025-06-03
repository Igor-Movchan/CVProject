FROM python:3.10.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      curl \
      # WeasyPrint dependencies:
      libcairo2 \
      libcairo2-dev \
      libpango-1.0-0 \
      libpango1.0-dev \
      libgdk-pixbuf2.0-0 \
      libgdk-pixbuf2.0-dev \
      libffi-dev \
      shared-mime-info && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --fake-initial && gunicorn CVProject.wsgi:application --bind 0.0.0.0:8000"]

