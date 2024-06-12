# Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

# Create and set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Copy .env file
COPY .env /code/.env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
