FROM python:3.10-slim

# ======================
# SYSTEM DEPENDENCIES
# ======================
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ======================
# WORKDIR
# ======================
WORKDIR /app

# ======================
# PYTHON DEPENDENCIES
# ======================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ======================
# COPY APP
# ======================
COPY . .

# ======================
# EXPOSE PORT
# ======================
EXPOSE 8000

# ======================
# RUN SERVER
# ======================
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
