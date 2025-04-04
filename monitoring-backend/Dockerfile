FROM python:3.11-slim

ENV PYTHONPATH="/monitoring-backend"

WORKDIR /monitoring-backend

COPY README.md pyproject.toml poetry.lock /monitoring-backend/

RUN pip install --no-cache-dir --upgrade poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY . /monitoring-backend

CMD ["python3", "start.py"]
