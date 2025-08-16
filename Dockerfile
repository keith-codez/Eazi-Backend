# Use an official lightweight Python image
FROM python:3.11-slim

# Set some environment variables so Python runs better inside Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Install some system tools (needed for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first, then install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Now copy the rest of your project files
COPY . .

# Expose port 8000 (Django’s default dev server port)
EXPOSE 8000

# Default command to run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
