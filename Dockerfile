FROM python:3.12.12-slim-bookworm

WORKDIR /app

EXPOSE 8000 

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
