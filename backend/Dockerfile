# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system deps first — cached separately from Python deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps before copying app code
# This layer is cached unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY artifacts/ ./artifacts/

RUN apt-get update && apt-get install -y curl

# Artifacts are mounted as a volume — not baked into the image
# This means you can update models without rebuilding the image
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]