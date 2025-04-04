FROM python:3.11-slim

ENV PYTHONPATH="/monitoring-backend"
ENV HOST="0.0.0.0"
ENV PORT=5487
ENV LOG_LEVEL="INFO"
ENV REFESH_FREQUENCY="10Hz"

WORKDIR /monitoring-backend

COPY README.md pyproject.toml poetry.lock /monitoring-backend/

RUN pip install --no-cache-dir --upgrade poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY . /monitoring-backend

RUN chmod +x start.sh

CMD ["./start.sh"]