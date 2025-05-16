FROM python:3.9-slim

RUN apt-get update && apt-get install -y sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

ENV PYTHONUNBUFFERED 1

# Install system dependencies required for Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000