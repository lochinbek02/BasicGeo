FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app
