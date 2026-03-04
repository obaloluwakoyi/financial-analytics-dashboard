FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# --- INSERT THE PRO-TIP HERE ---
RUN apt-get update && apt-get install -y build-essential --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# --- Dependency install (cache-friendly) ---
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --no-compile -r requirements.txt

# --- Copy application code ---
COPY . .

# ... rest of your file (chown, USER, EXPOSE, CMD)