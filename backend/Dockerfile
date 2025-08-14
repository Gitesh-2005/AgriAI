FROM python:3.11-slim

WORKDIR /AGRIAI

# Install build tools
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Install build tools first
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app","--host", "0.0.0.0","--port", "8000", "--reload"]