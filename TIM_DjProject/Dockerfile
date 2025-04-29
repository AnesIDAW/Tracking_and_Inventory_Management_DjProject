# Use official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /code/
COPY ./custom_jazzmin_templates/base.html /usr/local/lib/python3.12/site-packages/jazzmin/templates/admin/base.html


# Run Django server by default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
