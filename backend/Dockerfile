FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN git config --global --add safe.directory /app
RUN mkdir -p /var/log/sentinel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY core/ ./core/
COPY graph/ ./graph/
COPY runbooks/ ./runbooks/


EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
